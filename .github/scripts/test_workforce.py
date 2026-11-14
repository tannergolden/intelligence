#!/usr/bin/env python3
"""Tests for the workforce checker, renderer and installer.

WHY THIS EXISTS. The workforce is the source every environment's copy is
rendered from, so a rule `workforce.py check` stops enforcing is a rule
every copy quietly loses: a Director without its star, a team of six, a
name that looks right and holds a variation selector, a tool one API
rejects. And the installer writes into folders people keep their own
agents in, so it must never overwrite or remove a file that is not the
workforce's, nor carry the home kit's mark, which the kit's own sweep
would take out. These tests hold the real workforce to every check, prove
each check fails when its rule is broken, and run every install against a
throwaway home folder.

Run it:

    python3 .github/scripts/test_workforce.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent


def load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    # Dataclasses look their own module up by name while the class is built.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


wf = load('workforce', 'workforce.py')
install_py = load('install_for_workforce', 'install.py')

REAL = wf.ROOT / wf.SOURCE


def quiet(call, *args, **kwargs):
    """Run a call with its printing swallowed, and return what it returned."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return call(*args, **kwargs)


class Copy:
    """A throwaway copy of the real workforce, laid out as a repository root."""

    def __enter__(self) -> pathlib.Path:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        # Only the files git would commit: the copy has no git, so an ignored file such as an
        # editor's swap file would otherwise turn up in it as part of the source.
        for path in wf.source_files(REAL):
            target = self.root / wf.SOURCE / path.relative_to(REAL)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        return self.root

    def __exit__(self, *exc) -> None:
        self.tmp.cleanup()


def problems(root: pathlib.Path) -> list:
    return wf.problems_in(root / wf.SOURCE)[1]


def edit(path: pathlib.Path, old: str, new: str) -> None:
    text = path.read_text(encoding='utf-8')
    assert old in text, f'{old!r} not in {path}'
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


def set_field(path: pathlib.Path, key: str, value) -> None:
    """Rewrite one frontmatter field, whatever quoting the file uses; None removes it."""
    fields, body = wf.parse(path.read_text(encoding='utf-8'))
    if value is None:
        fields.pop(key)
    else:
        fields[key] = value
    lines = ['---'] + [f'{k}: {json.dumps(v, ensure_ascii=False)}' for k, v in fields.items()] + ['---', '', body]
    path.write_text('\n'.join(lines), encoding='utf-8')


def problems_of(source: pathlib.Path) -> list:
    return wf.problems_in(source)[1]


def retire(root: pathlib.Path, old: str, new: str) -> None:
    """Add one title to the copy's list of retired titles."""
    path = root / wf.SOURCE / wf.SETUP / wf.RETIRED
    data = json.loads(path.read_text(encoding='utf-8'))
    data['retired'][old] = new
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def set_raw(path: pathlib.Path, key: str, raw: str) -> None:
    """Replace one frontmatter line with raw text, quoting and all."""
    text = path.read_text(encoding='utf-8')
    new, count = re.subn(rf'^{key}: .*$', lambda _: f'{key}: {raw}', text, count=1, flags=re.M)
    assert count == 1, f'{key} not in {path}'
    path.write_text(new, encoding='utf-8')


class TheRealWorkforce(unittest.TestCase):
    def setUp(self) -> None:
        self.workforce, self.problems = wf.problems_in(REAL)

    def test_passes_every_check(self) -> None:
        self.assertEqual(self.problems, [])

    def test_mirrors_the_venture_template(self) -> None:
        folders = sorted(p.name for p in REAL.iterdir() if p.is_dir())
        self.assertEqual(folders, sorted(wf.DEPARTMENTS + (wf.CATCH_ALL, wf.SCHEMAS, wf.SETUP)))

    def test_every_retired_title_is_gone_and_its_successor_has_a_seat(self) -> None:
        self.assertTrue(self.workforce.retired)
        titles = {agent.name for agent in self.workforce.agents}
        for old, new in self.workforce.retired.items():
            self.assertNotIn(old, titles)
            self.assertTrue(new == '' or new in titles, (old, new))

    def test_each_department_has_one_starred_director_and_at_most_four_more(self) -> None:
        for folder in wf.DEPARTMENTS:
            team = self.workforce.team(folder)
            directors = [a for a in team if a.role == 'director']
            self.assertEqual(len(directors), 1, folder)
            expected = '\u2b50 Chief Executive Officer' if folder == wf.EXECUTIVE_TEAM else '\u2b50 Director of '
            self.assertTrue(directors[0].name.startswith(expected), folder)
            # Five in a department, and the Chief of Staff, fill a Grok Bot group of six.
            self.assertLessEqual(len(team), 5, folder)
            self.assertIs(team[0], directors[0], folder)

    def test_the_executive_team_runs_the_workforce_like_a_company(self) -> None:
        team = self.workforce.team(wf.EXECUTIVE_TEAM)
        ceo = team[0]
        self.assertEqual(ceo.fields['reports_to'], 'owner')
        for chief in team[1:]:
            self.assertEqual(chief.role, 'executive')
            self.assertTrue(chief.name.startswith('Chief '), chief.name)
            self.assertEqual(chief.fields['reports_to'], ceo.id)
            self.assertTrue(self.workforce.portfolio(chief), chief.name)
        overseen = [f for m in team for f in self.workforce.portfolio(m)]
        self.assertEqual(sorted(overseen), sorted(f for f in wf.DEPARTMENTS if f != wf.EXECUTIVE_TEAM))

    def test_only_agents_that_change_files_carry_the_repository_standards(self) -> None:
        for agent in self.workforce.agents:
            prompt = wf.compose(self.workforce, agent)
            self.assertEqual('# Repository Standards' in prompt, 'edit' in agent.fields['tools'], agent.name)

    def test_the_chief_of_staff_routes_from_every_row_of_every_charter(self) -> None:
        prompt = wf.compose(self.workforce, self.workforce.agent('chief-of-staff'))
        for folder, charter in self.workforce.charters.items():
            director = self.workforce.director(folder).name
            for function, owner in wf.coverage_rows(charter.body):
                label = 'Director' if owner == director else owner
                line = re.escape(f'**{folder}**: ') + r'[^\n]*' + re.escape(f'{label}: ') + r'[^\n]*'
                self.assertRegex(prompt, line + re.escape(function), folder)

    def test_every_title_has_at_least_two_words(self) -> None:
        for agent in self.workforce.agents:
            words = [word for word in agent.name.split() if re.search('[A-Za-z0-9]', word)]
            self.assertGreaterEqual(len(words), 2, agent.name)

    def test_the_root_holds_the_orchestrator_and_the_vault_manager(self) -> None:
        roots = sorted(a.name for a in self.workforce.agents if not a.department)
        self.assertEqual(roots, ['Chief of Staff', 'Knowledge Vault Manager'])

    def test_every_composed_prompt_holds_its_parts_in_order_and_fits(self) -> None:
        for agent in self.workforce.agents:
            prompt = wf.compose(self.workforce, agent)
            self.assertLessEqual(len(prompt), wf.MAX_PROMPT, agent.name)
            # The agent first, then its department, the protocol, the standards where it changes
            # files, and the directory last: a model weighs the start and the end of a prompt most.
            titles = [line[2:] for line, fenced in wf.scan(prompt) if not fenced and line.startswith('# ')]
            expected = ([agent.name] + ([agent.department] if agent.department else []) + ['Workforce Protocol']
                        + (['Repository Standards'] if 'edit' in agent.fields['tools'] else []) + ['The Workforce'])
            self.assertEqual(titles, expected, agent.name)
            self.assertTrue(prompt.startswith(f'# {agent.name}\n\n{agent.body.strip()}\n\n# '), agent.name)
            protocol = self.workforce.protocol.body.strip()
            self.assertIn(f'\n\n# Workforce Protocol\n\n{protocol}\n\n# ', prompt, agent.name)
            if agent.department:
                charter = self.workforce.charters[agent.department].body.strip()
                self.assertIn(f'\n\n# {agent.department}\n\n{charter}\n\n# Workforce Protocol\n', prompt, agent.name)
            last = prompt.rstrip('\n').rsplit('\n', 1)[1]
            self.assertTrue(last.startswith('You may message directly: '), agent.name)
            self.assertTrue(prompt.endswith('\n') and not prompt.endswith('\n\n'), agent.name)

    def test_the_directory_names_whom_each_agent_may_message(self) -> None:
        for agent in self.workforce.agents:
            last = wf.directory(self.workforce, agent).rstrip('\n').rsplit('\n', 1)[1]
            if agent.role == 'orchestrator':
                self.assertIn('every agent', last)
                continue
            named = last[len('You may message directly: '):].split('. Everyone else')[0].split(', ')
            self.assertEqual(named, [peer.name for peer in wf.peers(self.workforce, agent)], agent.name)
            self.assertTrue(last.endswith('Everyone else, through the Chief of Staff.'), agent.name)

    def test_the_directory_shows_who_oversees_each_department(self) -> None:
        text = wf.directory(self.workforce, self.workforce.agent('managing-editor'))
        rows = {cells[0]: cells for cells in ([cell.strip() for cell in line.strip('|').split('|')]
                                              for line in text.split('\n') if line.startswith('| '))}
        self.assertEqual(rows['Finance & Accounting (F&A)'][1:3], ['\u2b50 Director of Finance', 'Chief Financial Officer'])
        self.assertEqual(rows['Administration'][1:3], ['\u2b50 Chief Executive Officer', 'the owner'])
        self.assertEqual(set(rows) - {'Department', ':---'}, set(wf.DEPARTMENTS))
        # Every agent but the Chief of Staff gets each department's summary; it gets the full tables.
        self.assertEqual(rows['Department'], ['Department', 'Director', 'Overseen by', 'Covers'])
        hub = wf.directory(self.workforce, self.workforce.agent('chief-of-staff'))
        self.assertIn('| Department | Director | Overseen by |\n', hub)
        self.assertIn('## Who Owns What, Department By Department', hub)
        self.assertNotIn('## Who Owns What, Department By Department', text)

    def test_only_the_vault_manager_writes_the_vault_and_only_the_hub_asks_the_owner(self) -> None:
        for agent in self.workforce.agents:
            functions = wf.functions_for(agent)
            self.assertEqual('write_vault' in functions, agent.role == 'vault-manager', agent.name)
            self.assertEqual('request_owner_approval' in functions, agent.role == 'orchestrator', agent.name)

    def test_the_kit_mark_is_not_the_workforce_mark(self) -> None:
        # The home kit sweeps every agent file carrying its mark, so the two must never meet.
        self.assertNotIn(install_py.OWNED, wf.MARK)
        self.assertNotIn(wf.MARK, install_py.OWNED)


class TheTopology(unittest.TestCase):
    def setUp(self) -> None:
        self.workforce = wf.problems_in(REAL)[0]

    def ids(self, key: str) -> set:
        return {a.id for a in wf.peers(self.workforce, self.workforce.agent(key))}

    def test_a_specialist_reaches_its_department_and_the_hub_only(self) -> None:
        reach = self.ids('financial-analyst')
        team = {a.id for a in self.workforce.team('Finance & Accounting (F&A)')} - {'financial-analyst'}
        self.assertEqual(reach, team | {'chief-of-staff'})

    def test_a_director_reaches_no_other_department_and_not_its_chief(self) -> None:
        reach = self.ids('director-of-operations')
        self.assertNotIn('director-of-finance', reach)
        self.assertNotIn('chief-operating-officer', reach)
        self.assertIn('chief-of-staff', reach)

    def test_a_chief_reaches_the_executive_team_and_the_hub(self) -> None:
        team = {a.id for a in self.workforce.team(wf.EXECUTIVE_TEAM)} - {'chief-financial-officer'}
        self.assertEqual(self.ids('chief-financial-officer'), team | {'chief-of-staff'})

    def test_the_vault_manager_reaches_the_hub_alone(self) -> None:
        self.assertEqual(self.ids('knowledge-vault-manager'), {'chief-of-staff'})

    def test_the_hub_reaches_everyone(self) -> None:
        self.assertEqual(len(self.ids('chief-of-staff')), len(self.workforce.agents) - 1)


class EachCheckFails(unittest.TestCase):
    def assertProblem(self, root: pathlib.Path, pattern: str) -> None:
        found = problems(root)
        self.assertTrue(any(re.search(pattern, p) for p in found), f'no problem matched {pattern!r}: {found}')

    def test_a_director_without_its_star(self) -> None:
        with Copy() as root:
            folder = root / wf.SOURCE / 'Quality Assurance (QA)'
            old = folder / '\u2b50 Director of Quality Assurance.md'
            text = old.read_text(encoding='utf-8').replace('\u2b50 Director', 'Director')
            old.unlink()
            (folder / 'Director of Quality Assurance.md').write_text(text, encoding='utf-8')
            self.assertProblem(root, 'only its Director, takes the star')

    def test_a_star_with_a_variation_selector(self) -> None:
        with Copy() as root:
            folder = root / wf.SOURCE / 'Quality Assurance (QA)'
            old = folder / '\u2b50 Director of Quality Assurance.md'
            old.rename(folder / '\u2b50\ufe0f Director of Quality Assurance.md')
            self.assertProblem(root, 'variation selector')

    def test_a_title_of_one_word(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md'
            set_field(path, 'title', 'Editor')
            set_field(path, 'name', 'editor')
            path.rename(path.with_name('Editor.md'))
            self.assertProblem(root, r'Editor\.md: a title takes at least two words')

    def test_a_decomposed_name(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md'
            path.rename(path.with_name('Re\u0301sume\u0301 Editor.md'))
            self.assertProblem(root, 'not NFC')

    def test_an_underscore_in_a_name(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md'
            path.rename(path.with_name('Copy_Editor.md'))
            self.assertProblem(root, 'underscore')

    def test_a_sixth_agent(self) -> None:
        with Copy() as root:
            folder = root / wf.SOURCE / 'Sales & Marketing (S&M)'
            text = (folder / 'Account Executive.md').read_text(encoding='utf-8')
            (folder / 'Sales Engineer.md').write_text(text.replace('Account Executive', 'Sales Engineer'), encoding='utf-8')
            set_field(folder / 'Sales Engineer.md', 'name', 'sales-engineer')
            self.assertProblem(root, 'holds 6 agents')

    def test_a_charter_that_misses_an_agent(self) -> None:
        with Copy() as root:
            charter = root / wf.SOURCE / 'Human Resources (HR)' / 'Charter.md'
            members = wf.parse(charter.read_text(encoding='utf-8'))[0]['members']
            set_field(charter, 'members', [m for m in members if m != 'Health & Wellbeing Manager'])
            self.assertProblem(root, 'members must list exactly')

    def test_an_owner_from_another_department(self) -> None:
        with Copy() as root:
            charter = root / wf.SOURCE / 'Human Resources (HR)' / 'Charter.md'
            text = charter.read_text(encoding='utf-8')
            text, count = re.subn(r'^(\| The wellbeing program[^|]*\|)[^|]*\|$', r'\1 Financial Analyst |', text, flags=re.M)
            self.assertEqual(count, 1)
            charter.write_text(text, encoding='utf-8')
            self.assertProblem(root, 'outside the department')

    def test_a_name_that_is_not_the_slug_of_the_title(self) -> None:
        with Copy() as root:
            set_field(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', 'name', 'copy-editor')
            self.assertProblem(root, 'name must be "managing-editor"')

    def test_names_that_differ_only_in_case(self) -> None:
        # Names only, never the disk: a case-insensitive filesystem would hold one file, not two.
        found = wf.name_problems(['workforce/Public Relations (PR)/Managing Editor.md',
                                  'workforce/Public Relations (PR)/MANAGING EDITOR.md'])
        self.assertTrue(any('only in case' in problem for problem in found), found)

    def test_files_the_system_drops_never_fail_the_check(self) -> None:
        with Copy() as root:
            for name in ('.DS_Store', 'Thumbs.db', 'desktop.ini'):
                (root / wf.SOURCE / name).write_text('', encoding='utf-8')
                (root / wf.SOURCE / 'Administration' / name).write_text('', encoding='utf-8')
            self.assertEqual(problems(root), [])

    def test_the_check_reads_what_git_would_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / 'workforce'
            (root / 'Team').mkdir(parents=True)
            for name in ('Kept.md', 'Team/Kept Too.md', 'notes.swp', 'Team/.DS_Store', '.gitignore'):
                (root / name).write_text('*.swp\n' if name == '.gitignore' else 'x', encoding='utf-8')

            def names() -> list:
                return [path.relative_to(root).as_posix() for path in wf.source_files(root)]

            if wf.commit_of(root):
                self.skipTest('the temporary folder is inside a git checkout')
            # Outside a checkout: every file but those an operating system drops.
            self.assertEqual(names(), ['.gitignore', 'Kept.md', 'Team/Kept Too.md', 'notes.swp'])
            try:
                made = subprocess.run(['git', 'init', '--quiet', str(root.parent)], capture_output=True, check=False)
            except OSError:
                self.skipTest('git is not installed')
            self.assertEqual(made.returncode, 0, made.stderr)
            # Inside one: what git tracks or would add, so never a file `.gitignore` names.
            self.assertEqual(names(), ['.gitignore', 'Kept.md', 'Team/Kept Too.md'])

    def test_a_windows_device_name(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md'
            path.rename(path.with_name('Con.md'))
            self.assertProblem(root, 'device name')

    def test_a_path_too_long_for_windows(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md'
            path.rename(path.with_name('Editor ' + 'Of Very Long Titles ' * 8 + 'Today.md'))
            self.assertProblem(root, 'path is over 200')

    def test_an_unknown_capability(self) -> None:
        with Copy() as root:
            set_field(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', 'tools', ['teleport', 'read', 'message'])
            self.assertProblem(root, 'unknown tools teleport')

    def test_a_specialist_that_delegates(self) -> None:
        with Copy() as root:
            set_field(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', 'tools', ['delegate', 'read', 'message'])
            self.assertProblem(root, 'only the Chief of Staff and the Directors delegate')

    def test_an_em_dash(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', '## Mission\n\n', '## Mission\n\n\u2014 ')
            self.assertProblem(root, 'em dash')

    def test_a_second_title(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', '## Mission', '# Editor\n\n## Mission')
            self.assertProblem(root, 'holds a top-level heading')

    def test_an_executive_outside_the_executive_team(self) -> None:
        with Copy() as root:
            set_field(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', 'role', 'executive')
            self.assertProblem(root, 'executives sit in Administration')
            self.assertProblem(root, 'title starts with Chief')

    def test_a_director_that_reports_to_a_specialist(self) -> None:
        with Copy() as root:
            set_field(root / wf.SOURCE / 'Finance & Accounting (F&A)' / '\u2b50 Director of Finance.md',
                      'reports_to', 'financial-analyst')
            self.assertProblem(root, 'must name the member of Administration')

    def test_a_chief_with_no_departments(self) -> None:
        with Copy() as root:
            for folder in ('Information Technology (IT)', 'Research & Development (R&D)', 'Business Intelligence (BI)'):
                [director] = (root / wf.SOURCE / folder).glob('\u2b50 *.md')
                set_field(director, 'reports_to', 'chief-operating-officer')
            self.assertProblem(root, 'oversees no department')

    def test_a_missing_module(self) -> None:
        with Copy() as root:
            (root / wf.SOURCE / 'Repository Standards.md').unlink()
            self.assertProblem(root, 'Repository Standards.md: is missing')

    def test_a_file_that_names_a_retired_seat(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', '## Mission\n\n',
                 '## Mission\n\nSend every claim to the Fact-Checker. ')
            self.assertProblem(root, r'Editor\.md: names Fact-Checker, retired')

    def test_a_retired_title_inside_a_current_one_is_not_a_mention(self) -> None:
        # Marketing Manager is retired, and Digital Marketing Manager is a seat that names it in full.
        self.assertIn('Marketing Manager', wf.problems_in(REAL)[0].retired)
        self.assertEqual(problems_of(REAL), [])

    def test_a_retired_title_an_agent_still_carries(self) -> None:
        with Copy() as root:
            retire(root, 'Managing Editor', '')
            self.assertProblem(root, '"Managing Editor" is a title an agent carries')

    def test_a_retired_title_whose_successor_has_no_seat(self) -> None:
        with Copy() as root:
            retire(root, 'Town Crier', 'Herald')
            self.assertProblem(root, '"Town Crier" names "Herald" as the seat that took over')

    def test_a_setup_folder_missing_a_file(self) -> None:
        with Copy() as root:
            (root / wf.SOURCE / wf.SETUP / 'Terminal.md').unlink()
            self.assertProblem(root, 'setup/: must hold exactly')

    def test_a_setup_prompt_that_loses_a_part(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / wf.SETUP / 'Grok Bot.md', '</done_when>', '</done>')
            self.assertProblem(root, 'must open and close context, task, constraints, done_when once each')

    def test_a_setup_prompt_with_a_placeholder_nobody_is_told_to_fill(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / wf.SETUP / 'Grok Bot.md', '<task>\n', '<task>\nFor {{OWNER_NAME}}: ')
            self.assertProblem(root, 'must name exactly the placeholders the prompt holds')

    def test_a_setup_step_that_names_a_file_the_workforce_lacks(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / wf.SETUP / 'Grok Bot.md', '`workforce/setup/retired.json`',
                 '`workforce/schemas/retired.json`')
            self.assertProblem(root, 'names workforce/schemas/retired.json, which the workforce does not hold')

    def test_a_setup_prompt_that_does_not_name_its_own_steps(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / wf.SETUP / 'Terminal.md'
            text = path.read_text(encoding='utf-8')
            path.write_text(text.replace('workforce/setup/Terminal.md', 'the setup file'), encoding='utf-8')
            self.assertProblem(root, 'the prompt must name this file')

    def test_a_missing_section(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', '## Done When', '## Finished')
            self.assertProblem(root, 'missing sections Done When')

    def test_a_chief_of_staff_that_stops_keeping_the_workforce_current(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'Chief of Staff.md', '## Keeping The Workforce Current', '## Updates')
            self.assertProblem(root, 'missing sections Keeping The Workforce Current')

    def test_a_bare_value(self) -> None:
        with Copy() as root:
            set_raw(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', 'role', 'specialist')
            self.assertProblem(root, 'must hold a quoted string')

    def test_a_tool_keyword_one_api_rejects(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'schemas' / 'tools.json',
                 '"description": "The page\'s full https URL."',
                 '"description": "The page\'s full https URL.", "format": "uri"')
            self.assertProblem(root, 'web_fetch.url uses format')

    def test_an_optional_tool_parameter(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / 'schemas' / 'tools.json'
            data = json.loads(path.read_text(encoding='utf-8'))
            data['tools'][0]['parameters']['required'].remove('due')
            path.write_text(json.dumps(data), encoding='utf-8')
            self.assertProblem(root, 'must require every parameter')

    def test_a_team_in_the_catch_all(self) -> None:
        with Copy() as root:
            shutil.copy(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md',
                        root / wf.SOURCE / 'Miscellaneous' / 'Editor.md')
            self.assertProblem(root, 'it has no team')

    def test_a_folder_the_template_does_not_have(self) -> None:
        with Copy() as root:
            (root / wf.SOURCE / 'Agent Resources').mkdir()
            (root / wf.SOURCE / 'Agent Resources' / 'README.md').write_text('# Agent Resources\n', encoding='utf-8')
            self.assertProblem(root, 'not a folder of the venture template')

    def test_a_prompt_with_braces(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'Protocol.md', '## 1. Who You Serve\n', '## 1. Who You Serve\n\n{placeholder}\n')
            self.assertProblem(root, 'holds \\{ \\}')


PR = 'Public Relations (PR)'
EDITOR = f'{PR}/Managing Editor.md'
CHARTER = f'{PR}/Charter.md'
TOOLS = 'schemas/tools.json'
ENVELOPE = 'schemas/message.schema.json'


def at(root: pathlib.Path, rel: str) -> pathlib.Path:
    return root / wf.SOURCE / rel


def field(rel: str, key: str, value):
    return lambda root: set_field(at(root, rel), key, value)


def raw(rel: str, key: str, text: str):
    return lambda root: set_raw(at(root, rel), key, text)


def swap(rel: str, old: str, new: str):
    return lambda root: edit(at(root, rel), old, new)


def write(rel: str, text: str = ''):
    def change(root: pathlib.Path) -> None:
        at(root, rel).parent.mkdir(parents=True, exist_ok=True)
        at(root, rel).write_text(text, encoding='utf-8')
    return change


def garble(rel: str):
    """Leave a file that is not text: bytes no UTF-8 reader accepts."""
    return lambda root: at(root, rel).write_bytes(b'---\nname: \xff\xfe\n---\n')


def remove(rel: str):
    def change(root: pathlib.Path) -> None:
        path = at(root, rel)
        shutil.rmtree(path) if path.is_dir() else path.unlink()
    return change


def copy(source: str, target: str, **fields):
    def change(root: pathlib.Path) -> None:
        at(root, target).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(at(root, source), at(root, target))
        for key, value in fields.items():
            set_field(at(root, target), key, value)
    return change


def data(rel: str, change):
    """Change a JSON file in place through its parsed form; what the change returns is dropped."""
    def apply(root: pathlib.Path) -> None:
        loaded = json.loads(at(root, rel).read_text(encoding='utf-8'))
        change(loaded)
        at(root, rel).write_text(json.dumps(loaded), encoding='utf-8')
    return apply


def first_tool(change):
    return data(TOOLS, lambda loaded: change(loaded['tools'][0]))


def approval_tool(change):
    return data(TOOLS, lambda loaded: [change(tool) for tool in loaded['tools'] if tool['name'] == 'request_owner_approval'])


def members_reordered(root: pathlib.Path) -> None:
    members = wf.parse(at(root, CHARTER).read_text(encoding='utf-8'))[0]['members']
    set_field(at(root, CHARTER), 'members', members[1:] + members[:1])


def without_the_table(root: pathlib.Path) -> None:
    path = at(root, CHARTER)
    path.write_text('\n'.join(line for line in path.read_text(encoding='utf-8').split('\n')
                              if not line.startswith('|')), encoding='utf-8')


def editor_owns_nothing(root: pathlib.Path) -> None:
    path = at(root, CHARTER)
    path.write_text(re.sub(r'\| Managing Editor +\|', '| Content Producer |', path.read_text(encoding='utf-8')),
                    encoding='utf-8')


# Each rule of the check, broken once: what to change in a copy of the real workforce, and the
# problem the check must then report. A rule with no line here is a rule nothing holds.
BROKEN = [
    # An agent's frontmatter.
    ('a field the format does not have', field(EDITOR, 'nickname', 'Ed'), r'Managing Editor\.md: frontmatter must hold exactly'),
    ('a kind that is not agent', field(EDITOR, 'kind', 'module'), 'kind must be "agent"'),
    ('a title that is not the file name', field(EDITOR, 'title', 'Copy Chief'), 'title "Copy Chief" must equal the file name'),
    ('a title a name cannot hold', field(EDITOR, 'title', 'Managing  Editor'), 'title must be words, digits, single spaces'),
    ('a title that starts with a digit', copy(EDITOR, f'{PR}/2 Editors.md', title='2 Editors', name='2-editors'),
     r'2 Editors\.md: a title starts with a letter'),
    ('a role that is not one', field(EDITOR, 'role', 'editor'), 'role must be one of'),
    ('a root role inside a department', field(EDITOR, 'role', 'vault-manager'),
     'a department agent is a director, an executive or a specialist'),
    ('a file that is not text', garble(EDITOR), r'Managing Editor\.md: cannot be read'),
    ('an agent with no tools field', field(EDITOR, 'tools', None), 'tools must be a list of capabilities'),
    ('a department that is not its folder', field(EDITOR, 'department', 'Quality Assurance (QA)'),
     'department must be "Public Relations \\(PR\\)", its folder'),
    ('a star on a specialist', copy(EDITOR, f'{PR}/\u2b50 Managing Editor.md', title='\u2b50 Managing Editor'),
     'only its Director, takes the star'),
    ('a third agent at the root', copy(EDITOR, 'Managing Editor.md'), 'the root holds only Chief of Staff and Knowledge Vault Manager'),
    ('a root agent in a department role', field('Knowledge Vault Manager.md', 'role', 'specialist'),
     'the root holds only'),
    ('no orchestrator', remove('Chief of Staff.md'), 'the workforce needs exactly one orchestrator'),
    ('two agents under one name', copy(EDITOR, 'Quality Assurance (QA)/Managing Editor.md', department='Quality Assurance (QA)'),
     '"managing-editor" names two agents'),
    ('a department with no Director', field(f'{PR}/\u2b50 Director of Public Relations.md', 'role', 'specialist'),
     'needs exactly one Director, has 0'),
    ('a specialist that reports past its Director', field(EDITOR, 'reports_to', 'chief-of-staff'),
     'reports_to must be "director-of-public-relations"'),
    ('a vault manager that reports to the owner', field('Knowledge Vault Manager.md', 'reports_to', 'owner'),
     'reports_to must be "chief-of-staff"'),
    ('a specialist in the executive team', field('Administration/Chief Revenue Officer.md', 'role', 'specialist'),
     'every member of Administration but its Director is an executive'),
    ('tools that are one string', raw(EDITOR, 'tools', "'read'"), 'frontmatter key tools must hold a \\[list\\]'),
    ('a title that is a list', raw(EDITOR, 'title', "['Managing', 'Editor']"), 'frontmatter key title must hold one quoted string'),
    ('a capability named twice', field(EDITOR, 'tools', ['read', 'read', 'message']), 'tools lists a capability twice'),
    ('an agent that cannot message', field(EDITOR, 'tools', ['read', 'search']), 'every agent needs the message capability'),
    ('an agent with no tool an app knows', field(EDITOR, 'tools', ['message', 'tasks']), 'every agent needs the read capability'),
    ('a version that is not one', field(EDITOR, 'version', '1.0'), r'Managing Editor\.md: version must be MAJOR'),
    ('a version with a line after it', field(EDITOR, 'version', '1.0.0\n'), r'Managing Editor\.md: version must be MAJOR'),
    ('a version in other digits', field(EDITOR, 'version', '\u0661.\u0660.\u0660'), r'Managing Editor\.md: version must be MAJOR'),
    ('no description', field(EDITOR, 'description', ' '), 'needs a description'),
    ('a description with an angle bracket', field(EDITOR, 'description', 'Edits <everything>.'), 'must be one line of at most'),
    ('a description that is too long', field(EDITOR, 'description', 'Edits. ' * 200), 'must be one line of at most'),
    ('a description that splits a table', field(CHARTER, 'description', 'Press | and voice.'), 'without angle brackets or a vertical bar'),
    # Text no file may hold.
    ('a variation selector in a body', swap(EDITOR, '## Mission\n\n', '## Mission\n\n\u2b50\ufe0f '), 'U\\+FE0F; write the star'),
    ('a control character in a body', swap('Protocol.md', '## 1. Who You Serve\n', '## 1. Who You Serve\n\n\x1b[31mred\n'),
     r'Protocol\.md: holds U\+001B'),
    ('a delete character in a description', field(EDITOR, 'description', 'Edits\x7f everything.'), 'holds U\\+007F'),
    ('a character no one can see', swap(EDITOR, '## Mission\n\n', '## Mission\n\nEdits\u200beverything. '), 'holds U\\+200B'),
    ('a no-break space', swap(EDITOR, '## Mission\n\n', '## Mission\n\nEdits\u00a0everything. '), 'holds U\\+00A0'),
    ('half a surrogate pair', raw(EDITOR, 'description', '"Edits \\ud83d everything."'), 'holds U\\+D83D'),
    # Headings and sections.
    ('a top-level heading behind one space', swap(EDITOR, '## Mission', ' # Editor\n\n## Mission'), 'holds a top-level heading'),
    ('a top-level heading with a tab', swap(EDITOR, '## Mission', '#\tEditor\n\n## Mission'), 'holds a top-level heading'),
    ('a top-level heading underlined', swap(EDITOR, '## Mission', 'Editor\n======\n\n## Mission'), 'holds a top-level heading'),
    ('a section that is only in a code block', swap(EDITOR, '## Done When', '```text\n## Done When\n```'), 'missing sections Done When'),
    ('a vault manager that stops syncing context', swap('Knowledge Vault Manager.md', '## Keeping Context In Sync', '## Sync'),
     'missing sections Keeping Context In Sync'),
    ('a chief with nothing to oversee in its file', swap('Administration/Chief Revenue Officer.md', '## Overseeing Your Departments', '## Oversight'),
     'missing sections Overseeing Your Departments'),
    ('a director that does not lead', swap(f'{PR}/\u2b50 Director of Public Relations.md', '## Leading The Department', '## Leading'),
     'missing sections Leading The Department'),
    ('a prompt past the cap', swap(EDITOR, '## Mission\n\n', '## Mission\n\n' + 'Edit everything. ' * 2000), 'over the cap of 30000'),
    # A charter.
    ('a charter field the format lacks', field(CHARTER, 'owner', 'Nobody'), r'Charter\.md: frontmatter must hold exactly'),
    ('a charter of another kind', field(CHARTER, 'kind', 'agent'), 'kind must be "department"'),
    ('a charter titled for another folder', field(CHARTER, 'title', 'Press Office'), 'title must be "Public Relations \\(PR\\)", its folder'),
    ('a charter under another id', field(CHARTER, 'name', 'press'), 'name must be "public-relations"'),
    ('a charter naming the wrong Director', field(CHARTER, 'director', 'Managing Editor'), 'director must be'),
    ('a charter that lists its Director last', members_reordered, 'members must list the Director first'),
    ('a charter with a bad version', field(CHARTER, 'version', 'one'), r'Charter\.md: version must be MAJOR'),
    ('a charter with a title heading', swap(CHARTER, '## Mission', '# Public Relations\n\n## Mission'), r'Charter\.md: the body holds a top-level heading'),
    ('a charter without a section', swap(CHARTER, '## Scope', '## Range'), 'missing sections Scope'),
    ('a charter with no table', without_the_table, 'Who Owns What needs a table'),
    ('a member that owns nothing', editor_owns_nothing, 'Who Owns What gives nothing to Managing Editor'),
    ('a row with no function', swap(CHARTER, '## Inside The Department', '|  | Managing Editor |\n\n## Inside The Department'),
     'names an owner and no function'),
    # The shared modules.
    ('a module field the format lacks', field('Protocol.md', 'role', 'rules'), r'Protocol\.md: frontmatter must hold exactly'),
    ('a module under another id', field('Protocol.md', 'name', 'protocol'), 'name must be "workforce-protocol"'),
    ('a module with a bad version', field('Protocol.md', 'version', 'banana'), r'Protocol\.md: version must be MAJOR'),
    ('a module with a title heading', swap('Repository Standards.md', '## Where The Standards Are', '# Standards\n\n## Where The Standards Are'),
     r'Repository Standards\.md: the body holds a top-level heading'),
    ('a setup file with a bad version', field('setup/Grok Bot.md', 'version', '1'), r'Grok Bot\.md: version must be MAJOR'),
    ('a setup file under another id', field('setup/Terminal.md', 'name', 'cli'), 'name "terminal", its title as a slug'),
    ('a setup file of another kind', field('setup/Terminal.md', 'kind', 'module'), 'with kind "setup"'),
    ('a setup file with a title heading', swap('setup/Terminal.md', '## The Prompt', '# Terminal\n\n## The Prompt'),
     r'Terminal\.md: the body holds a top-level heading'),
    ('a setup file missing its steps', swap('setup/Terminal.md', '## The Steps', '## Steps'), 'missing sections The Steps'),
    ('a setup file with two prompts', swap('setup/Terminal.md', '## The Steps', '```text\nanother\n```\n\n## The Steps'),
     'must hold exactly one text block'),
    ('a setup prompt that never asks for what is unfilled', swap('setup/Terminal.md', 'still in double braces', 'left unfilled'),
     'must ask for any placeholder still in double braces'),
    ('a setup prompt with a stray brace', swap('setup/Terminal.md', '<task>\n', '<task>\n{target} '), 'holds a brace outside a placeholder'),
    ('a setup prompt that does not say when to use it', swap('setup/Terminal.md', '**Use when**', 'Use it when'), 'must say when to use it'),
    ('a list of retired titles that is not one', write('setup/retired.json', '{"retired": ["Editor"]}'), 'must hold "retired", an object'),
    ('a list of retired titles that is not JSON', write('setup/retired.json', '{'), r'retired\.json: is not valid JSON'),
    # The layout.
    ('a file at the root that is not Markdown', write('notes.txt', 'mine'), 'only Markdown sits at the root'),
    ('a folder inside a department', write(f'{PR}/drafts/Idea.md', 'x'), 'a department folder holds only Markdown files'),
    ('a file in a department that is not Markdown', write(f'{PR}/roster.csv', 'x'), 'a department folder holds only Markdown files'),
    ('no README at the root', remove('README.md'), r'workforce/README\.md: is missing'),
    ('a department that is gone', remove(PR), r'Public Relations \(PR\)/: the department folder is missing'),
    ('a department without its charter', remove(CHARTER), r'Charter\.md: is missing'),
    ('a department without its README', remove(f'{PR}/README.md'), r'Public Relations \(PR\)/README\.md: is missing'),
    ('a catch-all without its README', remove('Miscellaneous/README.md'), r'Miscellaneous/README\.md: is missing'),
    ('a stray file among the schemas', write('schemas/extra.json', '{}'), 'schemas/: must hold exactly'),
    # The tools and the envelope.
    ('tools that are not a list', write(TOOLS, '[]'), r'tools\.json: must hold "tools", a list of tools'),
    ('tools set to nothing', write(TOOLS, '{"tools": null}'), r'tools\.json: must hold "tools", a list of tools'),
    ('no tools at all', write(TOOLS, '{"tools": []}'), r'tools\.json: must hold "tools", a list of tools'),
    ('tools that are not JSON', write(TOOLS, '{'), r'tools\.json: is not valid JSON'),
    ('a tool named with a number', first_tool(lambda tool: tool.update(name=7)), 'tool name "7" must be lowercase letters'),
    ('a tool named in capitals', first_tool(lambda tool: tool.update(name='SendMessage')), 'must be lowercase letters'),
    ('a tool with a field of its own', first_tool(lambda tool: tool.update(strict=True)), 'must hold exactly name, description and parameters'),
    ('a tool whose parameters are a list', first_tool(lambda tool: tool.update(parameters=[])), 'parameters must be an object schema'),
    ('a tool whose properties are a list', first_tool(lambda tool: tool['parameters'].update(properties=[])), 'parameters must be an object schema'),
    ('a tool that allows other parameters', first_tool(lambda tool: tool['parameters'].update(additionalProperties=True)),
     'additionalProperties false'),
    ('a tool that requires nothing', first_tool(lambda tool: tool['parameters'].update(required=None)), 'must require every parameter'),
    ('a parameter with no description', first_tool(lambda tool: tool['parameters']['properties']['to'].pop('description')),
     r'\.to needs a description'),
    ('a parameter that is a string, not a schema', first_tool(lambda tool: tool['parameters']['properties'].update(to='text')),
     r'\.to needs a description'),
    ('a parameter of a type no API shares', first_tool(lambda tool: tool['parameters']['properties']['to'].update(type='object')),
     'must be a string, integer, number, boolean or array'),
    ('an array of something but strings', first_tool(lambda tool: tool['parameters']['properties']['to'].update(type='array', items={'type': 'integer'})),
     'may only be an array of strings'),
    ('an enum of numbers', first_tool(lambda tool: tool['parameters']['properties']['to'].update(enum=[1, 2])), 'enum must hold strings only'),
    ('a tool the capabilities grant, gone', data(TOOLS, lambda loaded: loaded['tools'].pop()), 'must define exactly the tools the capabilities grant'),
    ('an envelope that is a string', write(ENVELOPE, '"a message"'), r'message\.schema\.json: must hold a JSON Schema object'),
    ('an empty envelope', write(ENVELOPE, '{}'), r'message\.schema\.json: must hold a JSON Schema object'),
    ('an envelope without properties', data(ENVELOPE, lambda loaded: loaded.pop('properties')), 'must be a JSON Schema object with properties'),
    ('an envelope property that is a string', data(ENVELOPE, lambda loaded: loaded['properties'].update(state='any')),
     r'message\.schema\.json: state must list the values it takes'),
    ('an envelope that takes any state', data(ENVELOPE, lambda loaded: loaded['properties']['state'].pop('enum')),
     r'message\.schema\.json: state must list the values it takes'),
    ('a tool that offers a type the envelope refuses', data(ENVELOPE, lambda loaded: loaded['properties']['type']['enum'].pop()),
     "send_message type must offer exactly the envelope's values"),
    ('an approval tool with no gates', approval_tool(lambda tool: tool['parameters']['properties']['category'].pop('enum')),
     'request_owner_approval category must list the acts'),
]


class EveryRuleHolds(unittest.TestCase):
    """Break each rule once, and the check must name it. Nothing here may crash the check either:
    a file it cannot make sense of is a problem to list, never a traceback."""

    def test_each_rule_fails_when_it_is_broken(self) -> None:
        self.assertEqual(len({label for label, _, _ in BROKEN}), len(BROKEN), 'two cases share a label')
        for label, change, pattern in BROKEN:
            with self.subTest(label), Copy() as root:
                self.assertEqual(problems(root), [], 'the copy must start clean')
                change(root)
                found = problems(root)
                self.assertTrue(any(re.search(pattern, problem) for problem in found),
                                f'{label}: no problem matched {pattern!r}: {found}')

    def test_names_no_system_keeps_intact(self) -> None:
        self.assertEqual(wf.name_problems(['workforce/Sales & Marketing (S&M)/Managing Editor.md']), [])
        for path, pattern in (('workforce/Sales: Marketing.md', 'a character Windows refuses'),
                              ('workforce/Trailing Dot./A.md', r'Trailing Dot\.: .* ends in a space or a dot'),
                              ('workforce/Co\u2013Lead.md', 'an en or em dash'),
                              ('workforce/Co\u2014Lead.md', 'an en or em dash'),
                              ('workforce/' + 'x' * 256 + '.md', 'the name over 255 bytes'),
                              ('workforce/Caf\udce9.md', 'name is not valid UTF-8')):
            with self.subTest(path[:40]):
                found = wf.name_problems([path])
                self.assertTrue(any(re.search(pattern, problem) for problem in found), found)

    def test_a_comment_in_a_tilde_fence_is_not_a_heading(self) -> None:
        body = 'Text.\n\n~~~bash\n# a comment\n## not a section\n~~~\n\n````text\n```\n# still code\n````\n\n## Real\n'
        self.assertFalse(wf.has_title_heading(body))
        self.assertEqual(wf.sections(body), ['Real'])


class Parsing(unittest.TestCase):
    def test_slugs(self) -> None:
        self.assertEqual(wf.slug('\u2b50 Director of Research & Development'), 'director-of-research-and-development')
        self.assertEqual(wf.slug('Fact-Checker'), 'fact-checker')
        self.assertEqual(wf.department_id('Finance & Accounting (F&A)'), 'finance-and-accounting')

    def test_frontmatter_is_flat_json(self) -> None:
        fields, body = wf.parse('---\nname: "A"\ntools: ["read"]\n---\n\n# A\n')
        self.assertEqual(fields, {'name': 'A', 'tools': ['read']})
        self.assertEqual(body, '# A\n')

    def test_frontmatter_reads_the_layout_prettier_writes(self) -> None:
        text = "---\nname: 'a'\ntitle: \"Owner's Agent\"\ntools:\n  [\n    'read',\n    'web',\n  ]\n---\n# A\n"
        fields, _ = wf.parse(text)
        self.assertEqual(fields, {'name': 'a', 'title': "Owner's Agent", 'tools': ['read', 'web']})

    def test_a_list_item_may_hold_an_escaped_quote(self) -> None:
        fields, _ = wf.parse('---\nmembers: ["A \\"B\\" C", \'D, E\']\n---\n')
        self.assertEqual(fields['members'], ['A "B" C', 'D, E'])

    def test_frontmatter_refuses_what_it_cannot_read(self) -> None:
        for text in ('name: "A"\n', '---\nname: "A"\n', '---\nname: "A"\nname: "B"\n---\n', '---\nname A\n---\n',
                     '---\nname: A\n---\n', '---\nname: &anchor "A"\n---\n', "---\nname: 'it's'\n---\n"):
            with self.assertRaises(ValueError):
                wf.parse(text)


class Rendering(unittest.TestCase):
    def setUp(self) -> None:
        self.workforce = wf.problems_in(REAL)[0]

    def render(self, target: str, **options) -> dict:
        args = wf.argparse.Namespace(flavor='neutral', model=None, ref=None, grant=None)
        for key, value in options.items():
            setattr(args, key, value)
        return wf.render(self.workforce, target, args)

    def test_app_files_are_named_by_id_and_carry_the_mark(self) -> None:
        for target, suffix in (('claude', '.md'), ('grok-build', '.md'), ('copilot', '.agent.md'), ('codex', '.toml'),
                               ('antigravity', '.md')):
            files = self.render(target)
            self.assertEqual(len(files), len(self.workforce.agents), target)
            for name, text in files.items():
                # GitHub's Copilot agents take only these characters in a file name.
                self.assertRegex(name, r'^[A-Za-z0-9._-]+$', target)
                self.assertTrue(name.endswith(suffix), target)
                self.assertIn(wf.MARK, text, target)

    def frontmatter(self, text: str) -> tuple:
        """An app file as (its frontmatter's lines, its body)."""
        self.assertTrue(text.startswith('---\n'), text[:40])
        head, body = text[4:].split('\n---\n\n', 1)
        return head.split('\n'), body

    def test_each_app_file_is_its_frontmatter_then_the_composed_prompt(self) -> None:
        for target in ('claude', 'grok-build', 'copilot', 'antigravity'):
            files = self.render(target, grant=['read=connector_read'])
            for agent in self.workforce.agents:
                name = f'{agent.id}.agent.md' if target == 'copilot' else f'{agent.id}.md'
                lines, body = self.frontmatter(files[name])
                where = f'{target} {agent.name}'
                self.assertEqual(body, wf.compose(self.workforce, agent), where)
                self.assertEqual(lines[0], f'name: {agent.id}', where)
                key, _, value = lines[1].partition(': ')
                self.assertEqual((key, json.loads(value)), ('description', agent.fields['description']), where)
                # The mark closes the frontmatter as a comment, where the installer looks for it.
                self.assertEqual(lines[-1], f'# {wf.MARK}', where)
                keys = [line.split(':', 1)[0] for line in lines[2:-1]]
                expected = [] if target == 'grok-build' else ['tools']
                if target == 'antigravity' and agent.role == 'orchestrator':
                    expected.append('mainAgent')
                self.assertEqual(keys, expected, where)

    def test_copilot_tools_are_a_list_of_its_aliases(self) -> None:
        files = self.render('copilot', grant=['mail=mail/search'])
        lines, _ = self.frontmatter(files['full-stack-engineer.agent.md'])
        self.assertEqual(json.loads(lines[2].partition(': ')[2]), ['read', 'search', 'web', 'edit', 'execute'])
        lines, _ = self.frontmatter(files['chief-of-staff.agent.md'])
        tools = json.loads(lines[2].partition(': ')[2])
        self.assertIn('agent', tools)
        self.assertIn('mail/search', tools)
        self.assertNotIn('edit', tools)

    def test_claude_tools_follow_the_capabilities(self) -> None:
        files = self.render('claude')
        self.assertIn('tools: Read, Grep, Glob, WebFetch, WebSearch, Edit, Write, Bash\n',
                      files['full-stack-engineer.md'])
        self.assertIn('Agent', files['chief-of-staff.md'].split('---')[1])
        self.assertNotIn('Edit', files['financial-analyst.md'].split('---')[1])

    def test_a_grant_reaches_only_agents_with_the_capability(self) -> None:
        files = self.render('claude', grant=['mail=mcp__mail__search,mcp__mail__draft'])
        self.assertIn('mcp__mail__search, mcp__mail__draft', files['account-executive.md'].split('---')[1])
        self.assertNotIn('mcp__mail', files['financial-analyst.md'].split('---')[1])

    def test_grok_build_agents_inherit_their_tools(self) -> None:
        for text in self.render('grok-build').values():
            self.assertNotIn('\ntools:', text.split('\n---\n')[0])

    def test_codex_holds_the_composed_prompt(self) -> None:
        try:
            import tomllib
        except ImportError:
            self.skipTest('tomllib arrived in Python 3.11')
        files = self.render('codex')
        for agent in self.workforce.agents:
            text = files[f'{agent.id}.toml']
            self.assertEqual(text.split('\n')[0], f'# {wf.MARK}', agent.name)
            self.assertEqual(tomllib.loads(text), {
                'name': agent.id, 'description': agent.fields['description'],
                'developer_instructions': wf.compose(self.workforce, agent)}, agent.name)

    def test_a_toml_block_holds_any_text_exactly(self) -> None:
        try:
            import tomllib
        except ImportError:
            self.skipTest('tomllib arrived in Python 3.11')
        for value in ('plain\n', 'a \\ backslash and \\n that is not a line break\n', 'three """ quotes\n',
                      'ends in a quote"', 'ends in two""', '""""""', 'C:\\Users\\name\n', "single ''' quotes\n",
                      '\u2b50 Director of Finance, \u00e9 and \u00fc\n', '\nstarts with a line break\n'):
            self.assertEqual(tomllib.loads(f'x = {wf.toml_block(value)}\n')['x'], value, repr(value))

    def test_the_bundle_gives_each_agent_its_prompt_its_routes_and_its_tools(self) -> None:
        bundle = json.loads(self.render('bundle')['workforce.json'])
        self.assertEqual(bundle['format'], wf.FORMAT)
        self.assertEqual(bundle['flavor'], 'neutral')
        self.assertEqual(bundle['source'], {'repository': wf.REPOSITORY, 'path': wf.SOURCE,
                                            'commit': wf.commit_of(self.workforce.root)})
        self.assertEqual([entry['name'] for entry in bundle['agents']], [agent.id for agent in self.workforce.agents])
        for entry, agent in zip(bundle['agents'], self.workforce.agents):
            self.assertEqual(entry, {
                'name': agent.id, 'title': agent.name, 'role': agent.role,
                'department': wf.department_id(agent.department) if agent.department else None,
                'reports_to': agent.fields['reports_to'], 'description': agent.fields['description'],
                'capabilities': agent.fields['tools'],
                'may_message': [peer.id for peer in wf.peers(self.workforce, agent)],
                'tools': wf.functions_for(agent),
                'instructions': wf.compose(self.workforce, agent)}, agent.name)
        by_id = {entry['name']: entry for entry in bundle['agents']}
        # A host delivers a message only where may_message allows: a specialist's department and the hub.
        self.assertEqual(sorted(by_id['managing-editor']['may_message']),
                         ['chief-of-staff', 'communications-specialist', 'content-producer',
                          'director-of-public-relations'])
        self.assertEqual(by_id['knowledge-vault-manager']['may_message'], ['chief-of-staff'])
        self.assertEqual(by_id['full-stack-engineer']['tools'],
                         [name for capability in self.workforce.agent('full-stack-engineer').fields['tools']
                          for name in wf.FUNCTIONS[capability]])
        self.assertIn('write_file', by_id['full-stack-engineer']['tools'])
        self.assertNotIn('write_file', by_id['financial-analyst']['tools'])
        self.assertEqual([department['title'] for department in bundle['departments']], list(wf.DEPARTMENTS))
        for department in bundle['departments']:
            team = [agent.id for agent in self.workforce.team(department['title'])]
            self.assertEqual((department['members'], department['director']), (team, team[0]), department['title'])
            self.assertEqual(department['name'], wf.department_id(department['title']))
            self.assertEqual(department['description'],
                             self.workforce.charters[department['title']].fields['description'])
        self.assertEqual(bundle['tools'], self.workforce.tools)

    def test_the_bundle_carries_the_gates_and_an_envelope_a_validator_accepts(self) -> None:
        bundle = json.loads(self.render('bundle')['workforce.json'])
        approval = next(tool for tool in self.workforce.tools if tool['name'] == 'request_owner_approval')
        self.assertEqual(bundle['gates'], approval['parameters']['properties']['category']['enum'])
        self.assertGreaterEqual(len(bundle['gates']), 7)
        # `//` is the source's note, and no JSON Schema keyword: a strict validator refuses it.
        self.assertNotIn('//', bundle['envelope'])
        self.assertEqual(bundle['envelope']['$comment'], self.workforce.envelope['//'])
        self.assertEqual({key: value for key, value in bundle['envelope'].items() if key != '$comment'},
                         {key: value for key, value in self.workforce.envelope.items() if key != '//'})

    def test_the_bundle_holds_every_agent_tool_and_route(self) -> None:
        bundle = json.loads(self.render('bundle')['workforce.json'])
        self.assertEqual(len(bundle['agents']), len(self.workforce.agents))
        self.assertEqual(len(bundle['departments']), 12)
        defined = {tool['name'] for tool in bundle['tools']}
        ids = {agent['name'] for agent in bundle['agents']}
        for agent in bundle['agents']:
            self.assertLessEqual(set(agent['tools']), defined, agent['name'])
            self.assertLessEqual(set(agent['may_message']), ids, agent['name'])
        self.assertIn('\u2b50 Director of Finance', {agent['title'] for agent in bundle['agents']})
        finance = next(d for d in bundle['departments'] if d['title'] == 'Finance & Accounting (F&A)')
        self.assertEqual((finance['director'], finance['overseen_by']), ('director-of-finance', 'chief-financial-officer'))
        self.assertIn('properties', bundle['envelope'])

    def test_each_flavor_wraps_tools_its_own_way(self) -> None:
        # Each API refuses a tool with a key it does not know, so each shape is held exactly.
        for flavor, shape in (
                ('neutral', lambda tool: tool),
                ('responses', lambda tool: {'type': 'function', 'name': tool['name'],
                                            'description': tool['description'], 'parameters': tool['parameters']}),
                ('chat', lambda tool: {'type': 'function', 'function': tool}),
                ('anthropic', lambda tool: {'name': tool['name'], 'description': tool['description'],
                                            'input_schema': tool['parameters']}),
                ('mcp', lambda tool: {'name': tool['name'], 'description': tool['description'],
                                      'inputSchema': tool['parameters']})):
            bundle = json.loads(self.render('bundle', flavor=flavor)['workforce.json'])
            self.assertEqual(bundle['flavor'], flavor)
            self.assertEqual(bundle['tools'], [shape(tool) for tool in self.workforce.tools], flavor)
        self.assertEqual(sorted(wf.FLAVORS), ['anthropic', 'chat', 'mcp', 'neutral', 'responses'])

    def test_ollama_needs_a_model(self) -> None:
        with self.assertRaises(SystemExit):
            self.render('ollama')
        files = self.render('ollama', model='local-model')
        self.assertEqual(sorted(files), sorted(f'{agent.id}.Modelfile' for agent in self.workforce.agents))
        for agent in self.workforce.agents:
            self.assertEqual(files[f'{agent.id}.Modelfile'],
                             f'# {wf.MARK}\nFROM local-model\nSYSTEM """\n{wf.compose(self.workforce, agent)}"""\n')

    def test_text_mirrors_the_source_names(self) -> None:
        files = self.render('text')
        self.assertIn('Operations & Logistics (O&L)/\u2b50 Director of Operations.txt', files)
        self.assertIn('Chief of Staff.txt', files)
        self.assertEqual(len(files), len(self.workforce.agents))
        for agent in self.workforce.agents:
            folder = f'{agent.department}/' if agent.department else ''
            self.assertEqual(files[f'{folder}{agent.name}.txt'], wf.compose(self.workforce, agent), agent.name)

    def test_render_writes_each_file_into_the_folder_it_is_given(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp) / 'made' / 'here'
            self.assertEqual(quiet(wf.main, ['render', '--target', 'text', '--out', str(out)]), 0)
            written = sorted(path.relative_to(out).as_posix() for path in out.rglob('*') if path.is_file())
            self.assertEqual(written, sorted(self.render('text')))
            text = (out / 'Public Relations (PR)' / 'Managing Editor.txt').read_text(encoding='utf-8')
            self.assertEqual(text, wf.compose(self.workforce, self.workforce.agent('managing-editor')))

    def test_an_unknown_target_or_grant_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            self.render('notepad')
        for grant in ('fly=Jetpack', 'mail=', 'mail'):
            with self.assertRaises(SystemExit, msg=grant):
                self.render('claude', grant=[grant])
        self.assertEqual(wf.parse_grants(['mail=a, b', 'mail=c', 'read=d']), {'mail': ['a', 'b', 'c'], 'read': ['d']})

    def test_grok_bot_needs_a_version_outside_a_checkout(self) -> None:
        with Copy() as root:
            if wf.commit_of(root / wf.SOURCE):
                self.skipTest('the temporary folder is inside a git checkout')
            workforce = wf.problems_in(root / wf.SOURCE)[0]
            args = wf.argparse.Namespace(flavor='neutral', model=None, ref=None, grant=None, vault=None)
            with self.assertRaises(SystemExit) as refused:
                wf.render(workforce, 'grok-bot', args)
            self.assertIn('--ref', str(refused.exception))
            args.ref = 'v0'
            self.assertIn('/blob/v0/workforce/', wf.render(workforce, 'grok-bot', args)['Grok Bot Setup.md'])

    def test_antigravity_agents_get_tools_only_through_a_grant(self) -> None:
        plain = self.render('antigravity')
        self.assertTrue(all('\ntools:' not in text.split('\n---\n')[0] for text in plain.values()))
        self.assertIn('mainAgent: true', plain['chief-of-staff.md'].split('\n---\n')[0])
        self.assertNotIn('mainAgent', plain['financial-analyst.md'].split('\n---\n')[0])
        granted = self.render('antigravity', grant=['read=read_file'])
        self.assertIn('tools: ["read_file"]', granted['financial-analyst.md'])

    def test_grok_bot_pins_the_checkout_commit_by_default(self) -> None:
        commit = wf.commit_of(wf.ROOT)
        if not commit:
            self.skipTest('the source is not in a git checkout')
        page = self.render('grok-bot')['Grok Bot Setup.md']
        self.assertIn(f'/blob/{commit}/workforce/', page)

    def test_grok_bot_bindings_are_short_and_link_the_source(self) -> None:
        page = self.render('grok-bot', ref='v1.0.0')['Grok Bot Setup.md']
        self.assertEqual(len(re.findall(r'^### \d+\. ', page, re.M)), len(self.workforce.agents))
        for agent in self.workforce.agents:
            message = wf.binding(self.workforce, agent, 'v1.0.0', 'owner-name/knowledge-vault')
            self.assertLessEqual(len(message), 2000, agent.name)
            self.assertIn('/blob/v1.0.0/workforce/', message)
            self.assertEqual('Repository%20Standards.md' in message, 'edit' in agent.fields['tools'], agent.name)
            for url in re.findall(r'https://\S+', message):
                self.assertNotRegex(url, r'[ &()\u2b50]', url)
            # Every path a URL would have to encode comes with its link.
            for path in re.findall(r'^\d+\. (.+)$', message, re.M):
                self.assertEqual(bool(re.search(r'[^A-Za-z0-9/._-]', path)),
                                 f'{path}\n   https://' in message, path)

    def test_grok_bot_page_holds_the_prompt_with_the_version_filled_in(self) -> None:
        page = self.render('grok-bot', ref='v1.0.0')['Grok Bot Setup.md']
        prompt = page.split('## The Prompt', 1)[1].split('## The First Messages', 1)[0]
        self.assertIn('at the version v1.0.0.', prompt)
        self.assertNotIn('{{VERSION}}', page)
        # The vault is private, so a page rendered without its name leaves the placeholder to fill.
        self.assertIn('{{VAULT_REPOSITORY}}', prompt)
        named = self.render('grok-bot', ref='v1.0.0', vault='owner-name/knowledge-vault')['Grok Bot Setup.md']
        self.assertNotIn('{{', named)
        self.assertEqual(named.count('private GitHub repository owner-name/knowledge-vault'),
                         len(self.workforce.agents) + 1)

    def test_grok_bot_refuses_a_vault_that_is_not_a_repository_name(self) -> None:
        with self.assertRaises(SystemExit):
            quiet(self.render, 'grok-bot', ref='v1.0.0', vault='https://github.com/owner/vault')

    def test_only_the_vault_manager_is_told_it_writes_the_vault(self) -> None:
        for agent in self.workforce.agents:
            message = wf.binding(self.workforce, agent, 'v1.0.0', 'owner-name/knowledge-vault')
            self.assertEqual('you alone write to it' in message, agent.role == 'vault-manager', agent.name)
            self.assertEqual('never write to it' in message, agent.role != 'vault-manager', agent.name)
            # Every Bot but the Chief of Staff takes a new version from it, and nothing else.
            self.assertEqual('If the Chief of Staff sends this message again' in message,
                             agent.role != 'orchestrator', agent.name)


NUMBERS = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
TENS = {40: 'forty', 50: 'fifty', 60: 'sixty'}


def spelled(number: int) -> str:
    """A count from 40 to 69 as the documents write it."""
    tens, ones = number - number % 10, number % 10
    return TENS[tens] + (f'-{NUMBERS[ones - 1]}' if ones else '')


class TheDocuments(unittest.TestCase):
    """What the guide repeats from the source, it must repeat exactly: prompts, seats, lines and counts."""

    def setUp(self) -> None:
        self.workforce = wf.problems_in(REAL)[0]
        self.guide = (wf.ROOT / 'docs' / 'technical' / 'The-Workforce.md').read_text(encoding='utf-8')

    def row(self, first: str) -> list:
        """The cells of each of the guide's table rows that opens with this cell."""
        rows = [line for line in self.guide.split('\n') if line.startswith(f'| {first} ')]
        self.assertTrue(rows, first)
        return [[cell.strip() for cell in line.strip('|').split('|')] for line in rows]

    def test_the_guide_holds_each_setup_prompt_as_its_file_does(self) -> None:
        self.assertEqual(sorted(self.workforce.setups), sorted(wf.SETUPS))
        for name, setup in self.workforce.setups.items():
            prompt = wf.prompt_of(setup)
            self.assertTrue(prompt, name)
            self.assertIn(f'```text\n{prompt}\n```', self.guide, name)

    def test_the_first_message_template_keeps_every_fixed_line_of_the_binding(self) -> None:
        steps = self.workforce.setups['grok-bot'].body
        # The template names the vault as the steps do, so its line is held to the binding's too.
        message = wf.binding(self.workforce, self.workforce.agent('financial-analyst'), 'v1.0.0', '<owner/name>')
        fixed = [line.lstrip('- ').strip() for line in message.split('\n')
                 if line.strip() and 'Financial Analyst' not in line and 'workforce/' not in line
                 and 'Finance' not in line]
        self.assertGreaterEqual(len(fixed), 6)
        for line in fixed:
            self.assertIn(line, steps)

    def test_the_guide_gives_each_chief_the_departments_it_oversees(self) -> None:
        others = [f for f in wf.DEPARTMENTS if f != wf.EXECUTIVE_TEAM]
        for member in self.workforce.team(wf.EXECUTIVE_TEAM):
            oversees = self.workforce.portfolio(member)
            rows = [cells for cells in self.row(member.name) if len(cells) == 2]
            self.assertEqual(len(rows), 1, member.name)
            self.assertEqual([f for f in others if f in rows[0][1]], oversees, member.name)

    def test_the_guide_seats_each_department_as_the_source_does(self) -> None:
        for folder in wf.DEPARTMENTS:
            team = self.workforce.team(folder)
            rows = [cells for cells in self.row(folder) if len(cells) == 6]
            self.assertEqual(len(rows), 1, folder)
            seats, overseer, _, specialists = rows[0][1:5]
            self.assertEqual(seats, str(len(team)), folder)
            expected = 'The owner' if folder == wf.EXECUTIVE_TEAM else self.workforce.overseer(folder).name
            self.assertEqual(overseer, expected, folder)
            for agent in team[1:]:
                self.assertIn(agent.name, specialists, folder)

    def test_every_document_counts_the_agents_the_workforce_has(self) -> None:
        total = len(self.workforce.agents)
        seated = len([agent for agent in self.workforce.agents if agent.department])
        allowed = {spelled(total), spelled(seated)}
        count = re.compile(r'\b(?:forty|fifty|sixty)-(?:' + '|'.join(NUMBERS) + r')\b', re.I)
        # The research logs keep the counts of the day each entry was filed, so they are not held to this.
        for path in ('docs/technical/The-Workforce.md', 'docs/adrs/ADR-0044-The-Workforce-Lives-Beside-The-Kit.md',
                     'workforce/README.md', 'README.md'):
            text = (wf.ROOT / path).read_text(encoding='utf-8')
            for found in count.findall(text):
                self.assertIn(found.lower(), allowed, f'{path} counts {found}')
        self.assertIn(spelled(total).capitalize(), self.guide)


class Installing(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = pathlib.Path(self.tmp.name)
        self.agents = self.home / '.claude' / 'agents'

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_main(self, *argv: str, env: dict = None) -> int:
        return quiet(wf.main, list(argv), home=self.home, env=env if env is not None else {})

    def test_install_writes_every_agent(self) -> None:
        self.assertEqual(self.run_main('install', '--target', 'claude'), 0)
        self.assertEqual(len(list(self.agents.glob('*.md'))), len(wf.problems_in(REAL)[0].agents))

    def test_a_dry_run_changes_nothing(self) -> None:
        self.assertEqual(self.run_main('install', '--target', 'claude', '--dry-run'), 0)
        self.assertFalse(self.agents.exists())

    def snapshot(self) -> dict:
        return {path.name: path.read_bytes() for path in sorted(self.agents.iterdir())}

    def test_a_dry_run_over_an_install_changes_nothing(self) -> None:
        self.run_main('install', '--target', 'claude', '--grant', 'mail=mcp__mail__draft')
        retired = self.agents / 'retired-seat.md'
        retired.write_text(f'---\n# {wf.MARK}\n---\n', encoding='utf-8')
        (self.agents / 'financial-analyst.md').write_text(f'---\n# {wf.MARK}\n---\nstale\n', encoding='utf-8')
        before = self.snapshot()
        self.assertEqual(self.run_main('install', '--target', 'claude', '--dry-run', '--no-grants'), 0)
        self.assertEqual(self.run_main('uninstall', '--target', 'claude', '--dry-run'), 0)
        self.assertEqual(self.snapshot(), before)

    def test_install_honours_dest(self) -> None:
        elsewhere = self.home / 'elsewhere'
        self.assertEqual(self.run_main('install', '--target', 'claude', '--dest', str(elsewhere)), 0)
        self.assertTrue((elsewhere / 'chief-of-staff.md').is_file())
        self.assertFalse(self.agents.exists())
        self.assertEqual(self.run_main('uninstall', '--target', 'claude', '--dest', str(elsewhere)), 0)
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_each_target_installs_into_its_own_folder(self) -> None:
        for target, folder, name in (('claude', '.claude/agents', 'chief-of-staff.md'),
                                     ('grok-build', '.grok/agents', 'chief-of-staff.md'),
                                     ('copilot', '.copilot/agents', 'chief-of-staff.agent.md'),
                                     ('codex', '.codex/agents', 'chief-of-staff.toml')):
            self.assertEqual(self.run_main('install', '--target', target), 0, target)
            self.assertTrue((self.home / folder / name).is_file(), target)

    def test_install_never_writes_through_a_link(self) -> None:
        self.agents.mkdir(parents=True)
        outside = self.home / 'elsewhere'
        outside.mkdir()
        # One link to nothing, which looks like a free name, and one to a file of the owner's.
        (self.agents / 'financial-analyst.md').symlink_to(outside / 'not-there.md')
        mine = outside / 'notes.md'
        mine.write_text('mine\n', encoding='utf-8')
        (self.agents / 'tax-accountant.md').symlink_to(mine)
        self.assertEqual(self.run_main('install', '--target', 'claude'), 1)
        self.assertEqual(sorted(path.name for path in outside.iterdir()), ['notes.md'])
        self.assertEqual(mine.read_text(encoding='utf-8'), 'mine\n')
        self.assertTrue((self.agents / 'financial-analyst.md').is_symlink())
        # A link to one of the workforce's own files is still the owner's link: never swept, never removed.
        (self.agents / 'old-seat.md').symlink_to(self.agents / 'chief-of-staff.md')
        self.run_main('install', '--target', 'claude')
        self.run_main('uninstall', '--target', 'claude')
        self.assertTrue((self.agents / 'old-seat.md').is_symlink())

    def test_the_mark_counts_only_where_the_renderer_writes_it(self) -> None:
        self.agents.mkdir(parents=True)
        notes = self.agents / 'workforce-notes.md'
        notes.write_text('# My notes\n\n' + 'A line.\n' * 12 + f'The files say: {wf.MARK}\n# {wf.MARK}\n',
                         encoding='utf-8')
        self.assertFalse(wf.is_ours(notes))
        self.assertEqual(self.run_main('install', '--target', 'claude'), 0)
        self.assertEqual(self.run_main('uninstall', '--target', 'claude'), 0)
        self.assertTrue(notes.exists())
        for target in ('claude', 'copilot', 'codex', 'antigravity', 'grok-build'):
            suffix, locate = wf.INSTALLABLE[target]
            self.run_main('install', '--target', target)
            written = [path for path in sorted(locate(self.home, {}).glob(f'*{suffix}')) if path != notes]
            self.assertTrue(written and all(wf.is_ours(path) for path in written), target)

    def test_a_copy_the_owner_made_is_left_alone_once_installs_are_recorded(self) -> None:
        self.run_main('install', '--target', 'claude')
        copy = self.agents / 'my-analyst.md'
        copy.write_text((self.agents / 'financial-analyst.md').read_text(encoding='utf-8'), encoding='utf-8')
        self.assertEqual(self.run_main('install', '--target', 'claude'), 0)
        self.assertEqual(self.run_main('uninstall', '--target', 'claude'), 0)
        self.assertEqual([path.name for path in self.agents.iterdir()], ['my-analyst.md'])

    def test_a_recorded_file_the_workforce_dropped_is_removed(self) -> None:
        self.run_main('install', '--target', 'claude')
        record = json.loads((self.agents / wf.RECORD).read_text(encoding='utf-8'))
        record['targets']['claude']['files'] += ['retired-seat.md', 'someone-elses.md', '../outside.md']
        (self.agents / wf.RECORD).write_text(json.dumps(record), encoding='utf-8')
        (self.agents / 'retired-seat.md').write_text(f'---\n# {wf.MARK}\n---\n', encoding='utf-8')
        (self.agents / 'someone-elses.md').write_text('mine\n', encoding='utf-8')
        (self.home / '.claude' / 'outside.md').write_text(f'---\n# {wf.MARK}\n---\n', encoding='utf-8')
        self.assertEqual(self.run_main('install', '--target', 'claude'), 0)
        self.assertFalse((self.agents / 'retired-seat.md').exists())
        self.assertTrue((self.agents / 'someone-elses.md').exists())
        self.assertTrue((self.home / '.claude' / 'outside.md').exists())

    def test_grants_survive_a_plain_install_and_go_only_when_told(self) -> None:
        tools = lambda: (self.agents / 'account-executive.md').read_text(encoding='utf-8').split('---')[1]
        self.run_main('install', '--target', 'claude', '--grant', 'mail=mcp__mail__search,mcp__mail__draft')
        self.assertIn('mcp__mail__search, mcp__mail__draft', tools())
        self.assertEqual(self.run_main('install', '--target', 'claude'), 0)
        self.assertIn('mcp__mail__search, mcp__mail__draft', tools())
        self.run_main('install', '--target', 'claude', '--grant', 'mail=mcp__mail__read')
        self.assertIn('mcp__mail__read', tools())
        self.assertNotIn('mcp__mail__draft', tools())
        self.run_main('install', '--target', 'claude', '--no-grants')
        self.assertNotIn('mcp__mail', tools())
        self.run_main('install', '--target', 'claude')
        self.assertNotIn('mcp__mail', tools())

    def test_two_targets_in_one_folder_keep_to_their_own_files(self) -> None:
        shared = self.home / 'shared'
        self.run_main('install', '--target', 'copilot', '--dest', str(shared))
        self.run_main('install', '--target', 'claude', '--dest', str(shared))
        count = len(wf.problems_in(REAL)[0].agents)
        self.assertEqual(len(list(shared.glob('*.agent.md'))), count)
        self.run_main('uninstall', '--target', 'claude', '--dest', str(shared))
        self.assertEqual(len(list(shared.glob('*.agent.md'))), count)
        self.assertEqual([p.name for p in shared.glob('*.md') if not p.name.endswith('.agent.md')], [])
        # Before any record existed, a plain .md target still never took Copilot's files for its own.
        (shared / wf.RECORD).unlink()
        self.run_main('uninstall', '--target', 'claude', '--dest', str(shared))
        self.assertEqual(len(list(shared.glob('*.agent.md'))), count)

    def test_uninstall_runs_on_a_source_that_fails_the_check(self) -> None:
        self.run_main('install', '--target', 'claude')
        with Copy() as root:
            set_field(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', 'role', 'editor')
            self.assertEqual(quiet(wf.main, ['uninstall', '--target', 'claude'], root=root, home=self.home, env={}), 0)
        self.assertEqual(list(self.agents.iterdir()), [])

    def test_a_write_cut_short_leaves_the_old_file_whole(self) -> None:
        self.run_main('install', '--target', 'claude')
        target = self.agents / 'financial-analyst.md'
        before = target.read_text(encoding='utf-8')
        with self.assertRaises(UnicodeEncodeError):
            wf.write_atomic(target, 'half a file \ud83d')
        self.assertEqual(target.read_text(encoding='utf-8'), before)
        self.assertEqual([path.name for path in self.agents.iterdir() if path.name.endswith('.tmp')], [])

    def test_render_never_writes_over_an_agent_that_is_not_its_own(self) -> None:
        self.agents.mkdir(parents=True)
        mine = self.agents / 'security-engineer.md'
        mine.write_text('my own agent\n', encoding='utf-8')
        self.assertEqual(self.run_main('render', '--target', 'claude', '--out', str(self.agents)), 1)
        self.assertEqual(mine.read_text(encoding='utf-8'), 'my own agent\n')
        self.assertEqual([path.name for path in self.agents.iterdir()], ['security-engineer.md'])

    def test_install_never_overwrites_a_file_that_is_not_its_own(self) -> None:
        self.agents.mkdir(parents=True)
        mine = self.agents / 'financial-analyst.md'
        mine.write_text('my own analyst\n', encoding='utf-8')
        self.assertEqual(self.run_main('install', '--target', 'claude'), 1)
        self.assertEqual(mine.read_text(encoding='utf-8'), 'my own analyst\n')

    def test_install_removes_what_it_no_longer_ships_and_keeps_the_rest(self) -> None:
        self.agents.mkdir(parents=True)
        retired = self.agents / 'retired-seat.md'
        retired.write_text(f'---\n# {wf.MARK}\n---\n', encoding='utf-8')
        mine = self.agents / 'my-helper.md'
        mine.write_text('mine\n', encoding='utf-8')
        self.assertEqual(self.run_main('install', '--target', 'claude'), 0)
        self.assertFalse(retired.exists())
        self.assertTrue(mine.exists())

    def test_uninstall_takes_out_only_its_own(self) -> None:
        self.run_main('install', '--target', 'claude')
        mine = self.agents / 'my-helper.md'
        mine.write_text('mine\n', encoding='utf-8')
        self.assertEqual(self.run_main('uninstall', '--target', 'claude'), 0)
        self.assertEqual([p.name for p in self.agents.iterdir()], ['my-helper.md'])

    def test_antigravity_installs_into_its_global_agents_folder(self) -> None:
        self.assertEqual(self.run_main('install', '--target', 'antigravity'), 0)
        self.assertTrue((self.home / '.gemini' / 'config' / 'agents' / 'chief-of-staff.md').is_file())

    def test_codex_follows_codex_home(self) -> None:
        elsewhere = self.home / 'codex-home'
        self.run_main('install', '--target', 'codex', env={'CODEX_HOME': str(elsewhere)})
        self.assertTrue((elsewhere / 'agents' / 'chief-of-staff.toml').is_file())

    def test_the_kit_sweep_leaves_the_workforce_alone(self) -> None:
        self.run_main('install', '--target', 'claude')
        swept = install_py.leftovers(self.home, False, {})
        self.assertEqual([path for _, path in swept if path.parent == self.agents], [])

    def test_check_fails_on_a_broken_source(self) -> None:
        with Copy() as root:
            set_field(root / wf.SOURCE / 'Public Relations (PR)' / 'Managing Editor.md', 'role', 'editor')
            self.assertEqual(quiet(wf.main, ['check'], root=root), 1)
            self.assertEqual(quiet(wf.main, ['install', '--target', 'claude'], root=root, home=self.home), 1)
            self.assertFalse(self.agents.exists())


if __name__ == '__main__':
    unittest.main()
