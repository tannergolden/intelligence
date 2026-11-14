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
        shutil.copytree(REAL, self.root / wf.SOURCE)
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


def set_raw(path: pathlib.Path, key: str, raw: str) -> None:
    """Replace one frontmatter line with raw text, quoting and all."""
    text = path.read_text(encoding='utf-8')
    new, count = re.subn(rf'^{key}: .*$', f'{key}: {raw}', text, count=1, flags=re.M)
    assert count == 1, f'{key} not in {path}'
    path.write_text(new, encoding='utf-8')


class TheRealWorkforce(unittest.TestCase):
    def setUp(self) -> None:
        self.workforce, self.problems = wf.problems_in(REAL)

    def test_passes_every_check(self) -> None:
        self.assertEqual(self.problems, [])

    def test_mirrors_the_venture_template(self) -> None:
        folders = sorted(p.name for p in REAL.iterdir() if p.is_dir())
        self.assertEqual(folders, sorted(wf.DEPARTMENTS + (wf.CATCH_ALL, wf.SCHEMAS)))

    def test_each_department_has_one_starred_director_and_at_most_four_specialists(self) -> None:
        for folder in wf.DEPARTMENTS:
            team = self.workforce.team(folder)
            directors = [a for a in team if a.role == 'director']
            self.assertEqual(len(directors), 1, folder)
            self.assertTrue(directors[0].name.startswith('\u2b50 Director of '), folder)
            self.assertLessEqual(len(team), 5, folder)
            self.assertIs(team[0], directors[0], folder)

    def test_the_root_holds_the_orchestrator_and_the_vault_manager(self) -> None:
        roots = sorted(a.name for a in self.workforce.agents if not a.department)
        self.assertEqual(roots, ['Chief of Staff', 'Knowledge Vault Manager'])

    def test_every_composed_prompt_fits_and_ends_with_the_directory(self) -> None:
        for agent in self.workforce.agents:
            prompt = wf.compose(self.workforce, agent)
            self.assertLessEqual(len(prompt), wf.MAX_PROMPT, agent.name)
            self.assertTrue(prompt.startswith(f'# {agent.name}\n'), agent.name)
            self.assertIn('# Workforce Protocol', prompt)
            self.assertIn('You may message directly:', prompt)

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
        reach = self.ids('controller')
        team = {a.id for a in self.workforce.team('Finance & Accounting (F&A)')} - {'controller'}
        self.assertEqual(reach, team | {'chief-of-staff'})

    def test_a_director_reaches_no_other_department(self) -> None:
        reach = self.ids('director-of-operations')
        self.assertNotIn('director-of-finance', reach)
        self.assertIn('chief-of-staff', reach)

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
            self.assertProblem(root, 'only a Director, takes the star')

    def test_a_star_with_a_variation_selector(self) -> None:
        with Copy() as root:
            folder = root / wf.SOURCE / 'Quality Assurance (QA)'
            old = folder / '\u2b50 Director of Quality Assurance.md'
            old.rename(folder / '\u2b50\ufe0f Director of Quality Assurance.md')
            self.assertProblem(root, 'variation selector')

    def test_a_decomposed_name(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md'
            path.rename(path.with_name('Re\u0301sume\u0301 Editor.md'))
            self.assertProblem(root, 'not NFC')

    def test_an_underscore_in_a_name(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md'
            path.rename(path.with_name('Copy_Editor.md'))
            self.assertProblem(root, 'underscore')

    def test_a_sixth_agent(self) -> None:
        with Copy() as root:
            folder = root / wf.SOURCE / 'Finance & Accounting (F&A)'
            text = (folder / 'Controller.md').read_text(encoding='utf-8')
            (folder / 'Auditor.md').write_text(text.replace('Controller', 'Auditor'), encoding='utf-8')
            set_field(folder / 'Auditor.md', 'name', 'auditor')
            self.assertProblem(root, 'holds 6 agents')

    def test_a_charter_that_misses_an_agent(self) -> None:
        with Copy() as root:
            charter = root / wf.SOURCE / 'Human Resources (HR)' / 'Charter.md'
            members = wf.parse(charter.read_text(encoding='utf-8'))[0]['members']
            set_field(charter, 'members', [m for m in members if m != 'Wellbeing Specialist'])
            self.assertProblem(root, 'members must list exactly')

    def test_an_owner_from_another_department(self) -> None:
        with Copy() as root:
            charter = root / wf.SOURCE / 'Human Resources (HR)' / 'Charter.md'
            text = charter.read_text(encoding='utf-8')
            text, count = re.subn(r'^(\| Wellbeing program[^|]*\|)[^|]*\|$', r'\1 Controller |', text, flags=re.M)
            self.assertEqual(count, 1)
            charter.write_text(text, encoding='utf-8')
            self.assertProblem(root, 'outside the department')

    def test_a_name_that_is_not_the_slug_of_the_title(self) -> None:
        with Copy() as root:
            set_field(root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md', 'name', 'copy-editor')
            self.assertProblem(root, 'name must be "editor"')

    def test_names_that_differ_only_in_case(self) -> None:
        with Copy() as root:
            folder = root / wf.SOURCE / 'Public Relations (PR)'
            (folder / 'EDITOR.md').write_text((folder / 'Editor.md').read_text(encoding='utf-8'), encoding='utf-8')
            self.assertProblem(root, 'only in case')

    def test_a_windows_device_name(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md'
            path.rename(path.with_name('Con.md'))
            self.assertProblem(root, 'device name')

    def test_a_path_too_long_for_windows(self) -> None:
        with Copy() as root:
            path = root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md'
            path.rename(path.with_name('Editor ' + 'Of Very Long Titles ' * 8 + 'Today.md'))
            self.assertProblem(root, 'path is over 200')

    def test_an_unknown_capability(self) -> None:
        with Copy() as root:
            set_field(root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md', 'tools', ['teleport', 'read', 'message'])
            self.assertProblem(root, 'unknown tools teleport')

    def test_a_specialist_that_delegates(self) -> None:
        with Copy() as root:
            set_field(root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md', 'tools', ['delegate', 'read', 'message'])
            self.assertProblem(root, 'only the Chief of Staff and the Directors delegate')

    def test_an_em_dash(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md', '## Mission\n\n', '## Mission\n\n\u2014 ')
            self.assertProblem(root, 'em dash')

    def test_a_second_title(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md', '## Mission', '# Editor\n\n## Mission')
            self.assertProblem(root, 'holds a top-level heading')

    def test_a_missing_section(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md', '## Done When', '## Finished')
            self.assertProblem(root, 'missing sections Done When')

    def test_a_bare_value(self) -> None:
        with Copy() as root:
            set_raw(root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md', 'role', 'specialist')
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
            shutil.copy(root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md',
                        root / wf.SOURCE / 'Miscellaneous' / 'Editor.md')
            self.assertProblem(root, 'it has no team')

    def test_a_folder_the_template_does_not_have(self) -> None:
        with Copy() as root:
            (root / wf.SOURCE / 'Agent Resources').mkdir()
            self.assertProblem(root, 'not a folder of the venture template')

    def test_a_prompt_with_braces(self) -> None:
        with Copy() as root:
            edit(root / wf.SOURCE / 'Protocol.md', '## 1. Who You Serve\n', '## 1. Who You Serve\n\n{placeholder}\n')
            self.assertProblem(root, 'holds \\{ \\}')


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
        for target, suffix in (('claude', '.md'), ('grok-build', '.md'), ('copilot', '.agent.md'), ('codex', '.toml')):
            files = self.render(target)
            self.assertEqual(len(files), len(self.workforce.agents), target)
            for name, text in files.items():
                # GitHub's Copilot agents take only these characters in a file name.
                self.assertRegex(name, r'^[A-Za-z0-9._-]+$', target)
                self.assertTrue(name.endswith(suffix), target)
                self.assertIn(wf.MARK, text, target)

    def test_claude_tools_follow_the_capabilities(self) -> None:
        files = self.render('claude')
        self.assertIn('tools: Read, Grep, Glob, WebFetch, WebSearch, Edit, Write, Bash\n',
                      files['software-engineer.md'])
        self.assertIn('Agent', files['chief-of-staff.md'].split('---')[1])
        self.assertNotIn('Edit', files['controller.md'].split('---')[1])

    def test_a_grant_reaches_only_agents_with_the_capability(self) -> None:
        files = self.render('claude', grant=['mail=mcp__mail__search,mcp__mail__draft'])
        self.assertIn('mcp__mail__search, mcp__mail__draft', files['account-executive.md'].split('---')[1])
        self.assertNotIn('mcp__mail', files['controller.md'].split('---')[1])

    def test_grok_build_agents_inherit_their_tools(self) -> None:
        for text in self.render('grok-build').values():
            self.assertNotIn('\ntools:', text.split('\n---\n')[0])

    def test_codex_holds_the_composed_prompt(self) -> None:
        try:
            import tomllib
        except ImportError:
            self.skipTest('tomllib arrived in Python 3.11')
        files = self.render('codex')
        data = tomllib.loads(files['tax-strategist.toml'])
        self.assertEqual(data['name'], 'tax-strategist')
        self.assertEqual(data['developer_instructions'],
                         wf.compose(self.workforce, self.workforce.agent('tax-strategist')))

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
        self.assertIn('properties', bundle['envelope'])

    def test_each_flavor_wraps_tools_its_own_way(self) -> None:
        responses = json.loads(self.render('bundle', flavor='responses')['workforce.json'])['tools'][0]
        self.assertEqual(responses['type'], 'function')
        self.assertIn('parameters', responses)
        chat = json.loads(self.render('bundle', flavor='chat')['workforce.json'])['tools'][0]
        self.assertIn('parameters', chat['function'])
        anthropic = json.loads(self.render('bundle', flavor='anthropic')['workforce.json'])['tools'][0]
        self.assertIn('input_schema', anthropic)
        mcp = json.loads(self.render('bundle', flavor='mcp')['workforce.json'])['tools'][0]
        self.assertIn('inputSchema', mcp)

    def test_ollama_needs_a_model(self) -> None:
        with self.assertRaises(SystemExit):
            self.render('ollama')
        files = self.render('ollama', model='local-model')
        self.assertTrue(files['controller.Modelfile'].split('\n')[1] == 'FROM local-model')

    def test_text_mirrors_the_source_names(self) -> None:
        files = self.render('text')
        self.assertIn('Operations & Logistics (O&L)/\u2b50 Director of Operations.txt', files)
        self.assertIn('Chief of Staff.txt', files)

    def test_grok_bot_bindings_are_short_and_link_the_source(self) -> None:
        page = self.render('grok-bot', ref='v1.0.0')['Grok Bot Setup.md']
        self.assertEqual(page.count('\n## '), len(self.workforce.agents))
        for agent in self.workforce.agents:
            message = wf.binding(self.workforce, agent, 'v1.0.0')
            self.assertLessEqual(len(message), 2000, agent.name)
            self.assertIn('/blob/v1.0.0/workforce/', message)
            for url in re.findall(r'https://\S+', message):
                self.assertNotRegex(url, r'[ &()\u2b50]', url)


class TheGuide(unittest.TestCase):
    """The Grok Bot prompt in the guide restates the binding's rules, so the two must say the same."""

    def test_the_guide_template_keeps_every_fixed_line_of_the_binding(self) -> None:
        guide = (wf.ROOT / 'docs' / 'technical' / 'The-Workforce.md').read_text(encoding='utf-8')
        workforce = wf.problems_in(REAL)[0]
        message = wf.binding(workforce, workforce.agent('controller'), 'v1.0.0')
        fixed = [line.lstrip('- ').strip() for line in message.split('\n')
                 if line.strip() and 'Controller' not in line and 'workforce/' not in line
                 and 'Finance' not in line]
        self.assertTrue(fixed)
        for line in fixed:
            self.assertIn(line, guide)


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

    def test_install_never_overwrites_a_file_that_is_not_its_own(self) -> None:
        self.agents.mkdir(parents=True)
        mine = self.agents / 'controller.md'
        mine.write_text('my own controller\n', encoding='utf-8')
        self.assertEqual(self.run_main('install', '--target', 'claude'), 1)
        self.assertEqual(mine.read_text(encoding='utf-8'), 'my own controller\n')

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
            set_field(root / wf.SOURCE / 'Public Relations (PR)' / 'Editor.md', 'role', 'editor')
            self.assertEqual(quiet(wf.main, ['check'], root=root), 1)
            self.assertEqual(quiet(wf.main, ['install', '--target', 'claude'], root=root, home=self.home), 1)
            self.assertFalse(self.agents.exists())


if __name__ == '__main__':
    unittest.main()
