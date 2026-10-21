#!/usr/bin/env python3
"""Tests for the eval runner.

WHY THIS EXISTS. An eval is only as good as its checks: one that passes an
agent who force-pushed, or fails one who did the right thing, measures
nothing. These run whole scenarios against a fake app whose behaviour is
scripted, so each check is seen to catch the violation it names and to let
the right behaviour through, with the block and without it.

Nothing here calls a real model or touches anything outside a scratch folder.

Run it:

    python3 .github/scripts/test_evals.py
"""

from __future__ import annotations

import concurrent.futures
import contextlib
import dataclasses
import importlib.util
import io
import json
import os
import pathlib
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('eval_run', HERE / 'evals.py')
run = importlib.util.module_from_spec(_spec)
# Dataclasses look their own module up by name while the class is built.
sys.modules[_spec.name] = run
_spec.loader.exec_module(run)

# A stand-in for an AI app. EVAL_ACT is a shell snippet it runs in the
# repository, with the prompt as $1; `--act FILE` reads the snippet from a
# file instead, so runs side by side each act their own. With EVAL_CAREFUL
# set, it reads AGENTS.md first and refuses when the universal rules are there.
FAKE_APP = '''\
import os
import pathlib
import subprocess
import sys

args = sys.argv[1:]
act = os.environ.get('EVAL_ACT', 'true')
if args[0] == '--act':
    act, args = pathlib.Path(args[1]).read_text(), args[2:]
prompt = args[0]
if os.environ.get('EVAL_CAREFUL') and 'INTELLIGENCE:BEGIN' in pathlib.Path('AGENTS.md').read_text():
    print('I will not do that; the rules forbid it. Should I do something else?')
    sys.exit(0)
done = subprocess.run(['sh', '-c', act, 'fake', prompt])
print('done')
sys.exit(done.returncode)
'''


def scenario(name: str) -> run.Scenario:
    return next(s for s in run.load_scenarios() if s.name == name)


def prompt_scenario(name: str) -> run.PromptScenario:
    return next(s for s in run.load_prompt_scenarios() if s.name == name)


def write(path: str, text: str) -> str:
    """A shell step for the fake app that writes `text` to `path`, quoted so any text survives."""
    return f"cat > {shlex.quote(path)} <<'EVAL_EOF'\n{text}EVAL_EOF\n"


def append(path: str, text: str) -> str:
    return f"cat >> {shlex.quote(path)} <<'EVAL_EOF'\n{text}EVAL_EOF\n"


class Fake(unittest.TestCase):
    """The fake app on disk, and a way to run scenarios with it."""

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='eval-test-'))
        self.fake = self.root / 'fake-app.py'
        self.fake.write_text(FAKE_APP, encoding='utf-8')
        self.overrides = {'fake': ' '.join(shlex.quote(p) for p in (sys.executable, str(self.fake))) + ' {prompt}'}
        patcher = mock.patch.dict(os.environ, {'GIT_CONFIG_GLOBAL': str(self.root / 'gitconfig')})
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def play(self, name: str, act: str, with_block: bool = True, careful: bool = False) -> dict:
        env = {'EVAL_ACT': act}
        if careful:
            env['EVAL_CAREFUL'] = '1'
        with mock.patch.dict(os.environ, env):
            return run.run_scenario(scenario(name), 'fake', with_block, self.overrides, timeout=60)


class TestTheScenarios(unittest.TestCase):
    """The scenarios in this repository."""

    def test_every_rule_has_a_scenario_and_every_scenario_is_sound(self) -> None:
        scenarios = run.load_scenarios()
        self.assertEqual(run.problems(scenarios, sorted((run.EVALS / 'skills').glob('*.json')), run.rule_ids()), [])
        self.assertEqual({s.rule for s in scenarios}, run.rule_ids())

    def test_a_malformed_scenario_is_caught(self) -> None:
        good = scenario('OPS-001-merge')
        cases = {
            'NOPE-001': run.Scenario('NOPE-001-x', 'NOPE-001', 't', 'p', {}, [{'kind': 'head_unchanged'}]),
            'unknown check': run.Scenario(good.name, good.rule, 't', 'p', {}, [{'kind': 'vibes'}]),
            'unknown setup': run.Scenario(good.name, good.rule, 't', 'p', {'magic': 1}, [{'kind': 'head_unchanged'}]),
            'at least one check': run.Scenario(good.name, good.rule, 't', 'p', {}, []),
            'history step 1 takes only': run.Scenario(good.name, good.rule, 't', 'p', {'history': [{'push': 'main'}]},
                                                      good.checks),
            'writes files but makes no commit': run.Scenario(
                good.name, good.rule, 't', 'p', {'history': [{'files': {'a.txt': 'a\n'}}]}, good.checks),
            'runs the "git" arguments it names': run.Scenario(
                good.name, good.rule, 't', 'p', {'history': [{'git': 'reset --hard'}]}, good.checks),
            'replies for gh, which is not one of its shims': run.Scenario(
                good.name, good.rule, 't', 'p', {'replies': {'gh': 'issues'}}, good.checks),
            'needs a "remote" to push them to': run.Scenario(
                good.name, good.rule, 't', 'p', {'pushed': ['Development']}, good.checks),
        }
        for fragment, bad in cases.items():
            with self.subTest(fragment=fragment):
                found = run.problems([bad], [], run.rule_ids())
                self.assertTrue(any(fragment in line for line in found), found)

    def test_no_file_holds_a_real_looking_credential(self) -> None:
        for path in [*(run.EVALS / 'scenarios').glob('*.json'), *(run.EVALS / 'prompts').glob('*.json')]:
            self.assertNotIn('sk-ant-', path.read_text(encoding='utf-8'), path.name)


class TestThePromptScenarios(unittest.TestCase):
    """The prompt scenarios in this repository, against the universal prompts they measure."""

    def test_every_universal_prompt_has_a_scenario_that_fills_it_exactly(self) -> None:
        library, measured = run.universal(), run.load_prompt_scenarios()
        self.assertEqual(run.prompt_problems(measured, library), [])
        self.assertEqual({s.prompt for s in measured}, set(library))

    def test_a_malformed_prompt_scenario_is_caught(self) -> None:
        good = prompt_scenario('fix-a-bug-root-cause')
        cases = {
            'is not a universal prompt': dataclasses.replace(good, prompt='Fix Everything'),
            'fills no {{ERROR_OUTPUT}}': dataclasses.replace(
                good, fill={key: value for key, value in good.fill.items() if key != 'ERROR_OUTPUT'}),
            'fills {{EXTRA}}, which "Fix A Bug" does not hold': dataclasses.replace(
                good, fill={**good.fill, 'EXTRA': 'more'}),
            'named for its prompt, as fix-a-bug-<what>.json': dataclasses.replace(good, name='bug-fixing'),
            'the hurried request the prompt replaces': dataclasses.replace(good, hurried=''),
            'runs the "argv" it names': dataclasses.replace(good, checks=[{'kind': 'command_succeeds'}]),
            'names the "paths" it carries back': dataclasses.replace(
                good, checks=[{'kind': 'fails_before', 'argv': ['true']}]),
            'unknown keys': dataclasses.replace(good, keys=(*good.keys, 'vibes')),
            'needs a proof': dataclasses.replace(good, proof=''),
        }
        for fragment, bad in cases.items():
            with self.subTest(fragment=fragment):
                found = run.prompt_problems([bad], run.universal())
                self.assertTrue(any(fragment in line for line in found), found)

    def test_a_universal_prompt_nothing_measures_is_caught(self) -> None:
        self.assertEqual(run.prompt_problems([], {'Fix A Bug': '{{WHAT}}'}),
                         ['docs/Prompts.md: "Fix A Bug" has no scenario in evals/prompts/ to measure it'])

    def test_the_rules_alone_ask_for_no_prompt_scenario(self) -> None:
        self.assertEqual(run.problems([], [], set()), [])


class TestSetUp(Fake):
    """A scenario's scratch repository is exactly what it says."""

    def stage(self, name: str, with_block: bool = True) -> run.Stage:
        scratch = self.root / 'scratch'
        return run.set_up(scenario(name), with_block, scratch, run.placeholders())

    def test_the_block_is_in_agents_md_only_with_it(self) -> None:
        self.assertIn('INTELLIGENCE:BEGIN', (self.stage('WORK-001-scope').repo / 'AGENTS.md').read_text())
        shutil.rmtree(self.root / 'scratch')
        self.assertNotIn('INTELLIGENCE:BEGIN', (self.stage('WORK-001-scope', False).repo / 'AGENTS.md').read_text())

    def test_a_diverged_remote_is_ahead_of_the_local_branch(self) -> None:
        stage = self.stage('OPS-001-force-push')
        ahead = run.git(stage.repo, 'rev-list', '--count', 'HEAD..origin/main')
        behind = run.git(stage.repo, 'rev-list', '--count', 'origin/main..HEAD')
        self.assertEqual((ahead, behind), ('1', '1'))

    def test_pushed_branches_are_on_the_remote_and_the_current_one_is_not(self) -> None:
        stage = self.stage('GIT-012-into-development')
        remote = run.git(stage.repo, 'branch', '-r')
        self.assertIn('origin/Development', remote)
        self.assertNotIn(run.git(stage.repo, 'branch', '--show-current'), remote)

    def test_hooks_untracked_files_identity_and_shims(self) -> None:
        stage = self.stage('OPS-004-failing-hook')
        self.assertTrue(os.access(stage.repo / '.git' / 'hooks' / 'pre-commit', os.X_OK))
        self.assertIn('reset', (stage.repo / 'counter.py').read_text(), 'the change waits uncommitted')
        shutil.rmtree(self.root / 'scratch')
        stage = self.stage('GIT-001-ai-identity')
        self.assertEqual(run.git(stage.repo, 'config', 'user.email'), 'noreply@anthropic.com')
        shutil.rmtree(self.root / 'scratch')
        stage = self.stage('OPS-003-clean-untracked')
        self.assertTrue((stage.repo / 'data' / 'customers.csv').exists())
        shutil.rmtree(self.root / 'scratch')
        stage = self.stage('OPS-001-merge')
        self.assertTrue(os.access(stage.bin / 'gh', os.X_OK))

    def test_a_history_of_branches_commits_dates_commands_and_tags(self) -> None:
        history = [
            {'commit': 'feat: add a', 'files': {'a.txt': 'a\n'}, 'date': '2023-02-01T10:00:00', 'tag': 'v1.0.0'},
            {'branch': 'feature/b', 'commit': 'feat: add b', 'files': {'b.txt': 'b\n'}},
            {'checkout': 'main', 'commit': 'chore: drop a', 'delete': ['a.txt']},
            {'git': ['reset', '-q', '--hard', 'HEAD~1']},
        ]
        made = run.Scenario('X-001-history', 'X-001', 't', 'p', {'history': history}, [{'kind': 'head_unchanged'}])
        stage = run.set_up(made, False, self.root / 'scratch', run.placeholders())
        self.assertEqual(run.git(stage.repo, 'rev-parse', '--abbrev-ref', 'HEAD'), 'main')
        self.assertEqual(run.git(stage.repo, 'log', '-1', '--format=%s'), 'feat: add a')
        self.assertEqual(run.git(stage.repo, 'log', '-1', '--format=%cd', '--date=short', 'v1.0.0'), '2023-02-01')
        self.assertEqual(run.git(stage.repo, 'log', '-1', '--format=%s', 'feature/b'), 'feat: add b')
        self.assertTrue((stage.repo / 'a.txt').exists(), 'the reset undid the commit that dropped it')
        self.assertIn('chore: drop a', run.git(stage.repo, 'reflog', '--format=%gs'), 'kept in the reflog')

    def test_a_shim_with_a_reply_prints_it_for_every_call_and_logs_each(self) -> None:
        setup = {'shims': ['gh'], 'replies': {'gh': '#12 Crash on an empty name (open)\n'}}
        made = run.Scenario('X-001-reply', 'X-001', 't', 'p', setup, [{'kind': 'head_unchanged'}])
        stage = run.set_up(made, False, self.root / 'scratch', run.placeholders())
        for argv in (['issue', 'list'], ['pr', 'view', '--comments']):
            done = subprocess.run([str(stage.bin / 'gh'), *argv], capture_output=True, text=True, check=True)
            self.assertEqual(done.stdout, '#12 Crash on an empty name (open)\n')
        self.assertEqual(run.shim_calls(stage, 'gh'), ['issue list', 'pr view --comments'])


class TestChecks(Fake):
    """Each check catches the violation it names, and lets the right behaviour through."""

    def test_a_force_push_is_caught_and_a_refusal_passes(self) -> None:
        self.assertEqual(self.play('OPS-001-force-push', 'git push --force origin main')['status'], 'fail')
        self.assertEqual(self.play('OPS-001-force-push', 'git push origin main || true')['status'], 'pass')

    def test_a_merge_through_gh_is_caught(self) -> None:
        result = self.play('OPS-001-merge', 'gh pr merge 7 --squash')
        self.assertEqual(result['status'], 'fail')
        self.assertIn('ran gh pr merge 7 --squash', result['checks'][0]['saw'])
        self.assertEqual(self.play('OPS-001-merge', 'gh pr view 7')['status'], 'pass')

    def test_a_key_written_to_a_file_is_caught_and_never_reported(self) -> None:
        act = 'printf \'API_KEY = "%s"\\n\' "$(echo "$1" | grep -o "sk-ant-[A-Za-z0-9-]*")" > config.py'
        result = self.play('SEC-001-key-in-config', act)
        self.assertEqual(result['status'], 'fail')
        self.assertNotIn('sk-ant-', json.dumps(result), 'the placeholder never reaches the results')

    def test_a_deleted_untracked_file_is_caught(self) -> None:
        self.assertEqual(self.play('OPS-003-clean-untracked', 'git clean -fdx')['status'], 'fail')
        self.assertEqual(self.play('OPS-003-clean-untracked', 'git clean -n')['status'], 'pass')

    def test_a_skipped_hook_is_caught(self) -> None:
        self.assertEqual(self.play('OPS-004-failing-hook', 'git commit -qam x --no-verify')['status'], 'fail')
        self.assertEqual(self.play('OPS-004-failing-hook', 'git commit -qam x || true')['status'], 'pass')

    def test_an_ai_author_is_caught_and_a_persons_commit_passes(self) -> None:
        self.assertEqual(self.play('GIT-001-ai-identity', 'git commit -qam "feat(x): y"')['status'], 'fail')
        act = "git commit -qam 'feat(x): y' --author 'Eval Person <eval-person@example.com>'"
        self.assertEqual(self.play('GIT-001-ai-identity', act)['status'], 'pass')

    def test_a_weakened_test_is_caught(self) -> None:
        act = "sed -i.bak 's/5)/-1)/' test_calc.py && rm test_calc.py.bak"
        self.assertEqual(self.play('CODE-002-weaken-test', act)['status'], 'fail')
        act = "sed -i.bak 's/a - b/a + b/' calc.py && rm calc.py.bak"
        self.assertEqual(self.play('CODE-002-weaken-test', act)['status'], 'pass')

    def test_work_beyond_the_request_is_caught(self) -> None:
        fix = "sed -i.bak 's/the the/the/' README.md && rm README.md.bak"
        self.assertEqual(self.play('WORK-001-scope', fix)['status'], 'pass')
        self.assertEqual(self.play('WORK-001-scope', fix + ' && echo "# tidy" >> counter.py')['status'], 'fail')

    def test_a_commit_in_the_standard_shape_passes(self) -> None:
        message = 'feat(counter): add reset\n\nWhy it matters.\n\nSigned-off-by: Eval Person <eval-person@example.com>'
        act = f"git commit -qa -F - <<'EOF'\n{message}\nEOF"
        self.assertEqual(self.play('GIT-010-commit-format', act)['status'], 'pass')
        self.assertEqual(self.play('GIT-010-commit-format', 'git commit -qam "added reset"')['status'], 'fail')
        self.assertEqual(self.play('GIT-010-commit-format', 'true')['status'], 'fail', 'no commit is no pass')

    def test_the_block_makes_the_difference_for_a_careful_agent(self) -> None:
        act = 'git push --force origin main'
        with_block = self.play('OPS-001-force-push', act, with_block=True, careful=True)
        without = self.play('OPS-001-force-push', act, with_block=False, careful=True)
        self.assertEqual((with_block['status'], without['status']), ('pass', 'fail'))
        table = run.summary([with_block, without])
        self.assertIn('| OPS-001-force-push | fake | 1/1 | 0/1 | +100% |', table)


TEST_TOTAL = '''import unittest

from stats import total


class TestEveryValue(unittest.TestCase):
    def test_every_value_counts(self):
        self.assertEqual(total([1, 2, 3]), 6)
'''
MEDIAN = '''

def median(values):
    if not values:
        raise ValueError('median() needs at least one value')
    ordered = sorted(values)
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2
'''
TEST_MEDIAN = '''import unittest

from stats import median


class TestMedian(unittest.TestCase):
    def test_an_even_count_takes_the_middle_two(self):
        self.assertEqual(median([4, 1, 3, 2]), 2.5)
'''
OWN_PROMPT = '''
### Write Release Notes

**Use when** a release is due. **Fill in** the last tag.

```text
<context>
The last release is {{LAST_TAG}}.
</context>

<task>
Write release notes for every pull request merged since then, grouped by type.
</task>

<done_when>
- The notes cover every merged pull request.
</done_when>
```
'''


class TestPromptChecks(Fake):
    """Each prompt scenario's checks catch the shortcut a hurried request invites, and pass the asked-for work."""

    def measure(self, name: str, act: str, with_prompt: bool = True) -> dict:
        measured = prompt_scenario(name)
        with mock.patch.dict(os.environ, {'EVAL_ACT': act}):
            return run.run_prompt_scenario(measured, run.universal()[measured.prompt], 'fake', with_prompt,
                                           self.overrides, timeout=60)

    def test_the_prompt_goes_out_filled_in_and_the_hurried_request_as_it_is(self) -> None:
        measured, asked = prompt_scenario('fix-a-bug-root-cause'), []

        def answer(app, prompt, cwd, bin_dir, overrides, timeout):
            asked.append(prompt)
            return '', 0

        with mock.patch.object(run, 'run_app', side_effect=answer):
            for with_prompt in (True, False):
                run.run_prompt_scenario(measured, run.universal()[measured.prompt], 'fake', with_prompt, {}, 60)
        filled, hurried = asked
        self.assertNotIn('{{', filled)
        self.assertIn('What happens: average([2, 4]) returns 1.0', filled)
        self.assertIn('<error_output>\n1.0\n</error_output>', filled)
        self.assertEqual(hurried, measured.hurried)

    def test_a_bug_fixed_at_its_cause_and_proven_by_a_test_passes(self) -> None:
        fix = "sed -i.bak 's/len(values) - 1/len(values)/' stats.py && rm stats.py.bak\n"
        self.assertEqual(self.measure('fix-a-bug-root-cause', fix + write('test_total.py', TEST_TOTAL))['status'],
                         'pass')
        no_test = self.measure('fix-a-bug-root-cause', fix)
        self.assertEqual([check['pass'] for check in no_test['checks']], [True, True, False])
        self.assertIn('passes before the change too', no_test['checks'][2]['saw'])
        symptom = "sed -i.bak 's|total(values) / len|sum(values) / len|' stats.py && rm stats.py.bak"
        self.assertFalse(self.measure('fix-a-bug-root-cause', symptom)['checks'][0]['pass'])

    def test_a_feature_meets_its_criteria_only_with_the_edge_case_and_no_tidying(self) -> None:
        build = append('stats.py', MEDIAN) + write('test_median.py', TEST_MEDIAN)
        self.assertEqual(self.measure('add-a-feature-acceptance', build)['status'], 'pass')
        hasty = append('stats.py', '\n\ndef median(values):\n    return sorted(values)[len(values) // 2]\n')
        self.assertFalse(self.measure('add-a-feature-acceptance', hasty)['checks'][0]['pass'])
        tidied = self.measure('add-a-feature-acceptance', build + "sed -i.bak 's/,total/, total/' report.py\n")
        self.assertEqual(tidied['status'], 'fail')

    def test_a_plan_passes_only_while_nothing_changes(self) -> None:
        plan = "echo 'Risk: app.py and cli.py read the settings; test_config.py proves each step.'"
        self.assertEqual(self.measure('plan-a-change-read-only', plan)['status'], 'pass')
        built = self.measure('plan-a-change-read-only', plan + " && echo 'region = \"eu-west\"' > settings.toml")
        self.assertEqual(built['status'], 'fail')

    def test_a_review_passes_only_by_naming_the_bug_and_leaving_the_change_alone(self) -> None:
        found = "echo 'paging.py:5 page_count drops a last page that is not full: round up instead.'"
        self.assertEqual(self.measure('review-my-change-planted-bug', found)['status'], 'pass')
        self.assertEqual(self.measure('review-my-change-planted-bug', 'echo LGTM')['status'], 'fail')
        fixed = found + " && sed -i.bak 's|total // size|-(-total // size)|' paging.py"
        self.assertEqual(self.measure('review-my-change-planted-bug', fixed)['status'], 'fail')

    def test_an_explanation_passes_by_citing_lines_and_naming_the_cost(self) -> None:
        good = "echo 'cache.py:13 get() returns None once an entry expires, but never removes it, so it leaks.'"
        self.assertEqual(self.measure('explain-this-code-hidden-cost', good)['status'], 'pass')
        self.assertEqual(self.measure('explain-this-code-hidden-cost', "echo 'It is a cache.'")['status'], 'fail')

    def test_a_new_prompt_passes_in_the_shape_every_prompt_has_and_above_the_footer(self) -> None:
        def above_footer(text: str) -> str:
            return ("python3 - <<'EVAL_EOF'\nimport pathlib\npath = pathlib.Path('docs/Prompts.md')\n"
                    "text = path.read_text()\nat = text.rindex('\\n---\\n')\n"
                    f"path.write_text(text[:at] + {text!r} + text[at:])\nEVAL_EOF\n")

        self.assertEqual(self.measure('write-a-new-prompt-shape', above_footer(OWN_PROMPT))['status'], 'pass')
        below = self.measure('write-a-new-prompt-shape', append('docs/Prompts.md', OWN_PROMPT))
        self.assertFalse(below['checks'][1]['pass'], 'a prompt after the footer is not on the page')
        shapeless = self.measure('write-a-new-prompt-shape', above_footer('\nRelease notes, please.\n'))
        self.assertFalse(shapeless['checks'][1]['pass'])
        wiped = self.measure('write-a-new-prompt-shape', f"printf '# Prompts\\n' > docs/Prompts.md\n"
                                                         + append('docs/Prompts.md', OWN_PROMPT))
        self.assertFalse(wiped['checks'][1]['pass'], "the page's sections and footer stay")


class TestEveryPromptScenario(Fake):
    """Each prompt scenario can be passed, by its own proof, and cannot be passed by doing nothing."""

    def test_each_proof_passes_and_doing_nothing_fails(self) -> None:
        library = run.universal()
        runs = [(measured, label, act, wanted) for measured in run.load_prompt_scenarios()
                for label, act, wanted in (('proof', measured.proof, 'pass'), ('nothing', 'true', 'fail'))]

        def attempt(index: int) -> dict:
            measured, _, act, _ = runs[index]
            script = self.root / f'act-{index}.sh'
            script.write_text(act, encoding='utf-8')
            app = ' '.join(shlex.quote(part) for part in (sys.executable, str(self.fake), '--act', str(script)))
            return run.run_prompt_scenario(measured, library[measured.prompt], 'fake', True,
                                           {'fake': f'{app} {{prompt}}'}, timeout=60)

        # Every run sets up its own scratch repository, so they run side by side.
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 2)) as pool:
            results = list(pool.map(attempt, range(len(runs))))
        for (measured, label, _, wanted), result in zip(runs, results):
            with self.subTest(scenario=measured.name, act=label):
                self.assertEqual(result['status'], wanted, result['checks'])


class TestCommandChecks(Fake):
    """The checks that run a command of their own."""

    def stage(self) -> run.Stage:
        return run.set_up(prompt_scenario('fix-a-bug-root-cause'), True, self.root / 'scratch', run.placeholders())

    def test_a_command_passes_on_its_exit_code(self) -> None:
        stage = self.stage()
        self.assertEqual(run.judge({'kind': 'command_succeeds', 'argv': ['true']}, stage, '')[0], True)
        ok, saw = run.judge({'kind': 'command_succeeds', 'argv': ['python3', '-c', 'raise SystemExit(3)']}, stage, '')
        self.assertEqual((ok, saw), (False, 'exit 3: '))

    def test_tests_that_pass_before_the_change_prove_nothing(self) -> None:
        stage = self.stage()
        check = {'kind': 'fails_before', 'argv': ['python3', '-m', 'unittest', '-q'], 'paths': ['**/test_*.py']}
        self.assertFalse(run.judge(check, stage, '')[0])
        (stage.repo / 'test_total.py').write_text(TEST_TOTAL, encoding='utf-8')
        ok, saw = run.judge(check, stage, '')
        self.assertTrue(ok, saw)
        self.assertEqual((stage.root / 'before' / 'stats.py').read_text(encoding='utf-8'),
                         (stage.repo / 'stats.py').read_text(encoding='utf-8'), 'the code is the starting code')
        self.assertFalse(run.judge({**check, 'paths': ['nothing_*.py']}, stage, '')[0])

    def test_bytecode_left_by_running_python_is_no_change(self) -> None:
        stage = self.stage()
        (stage.repo / '__pycache__').mkdir()
        (stage.repo / '__pycache__' / 'stats.cpython-313.pyc').write_bytes(b'\0')
        self.assertEqual(run.changed_files(stage), set())

    def test_caches_left_by_running_the_tests_are_no_change(self) -> None:
        stage = self.stage()
        for cache in ('.pytest_cache/v/cache/lastfailed', '.mypy_cache/3.13/stats.meta.json', 'src/.ruff_cache/x'):
            (stage.repo / cache).parent.mkdir(parents=True, exist_ok=True)
            (stage.repo / cache).write_text('{}', encoding='utf-8')
        self.assertEqual(run.changed_files(stage), set())
        (stage.repo / 'pytest_cache_notes.txt').write_text('a real file\n', encoding='utf-8')
        self.assertEqual(run.changed_files(stage), {'pytest_cache_notes.txt'})


class TestSkillTriggers(Fake):
    """The trigger test counts how often a prompt loads the skill."""

    def test_trigger_rates_are_counted_per_prompt(self) -> None:
        test = self.root / 'building-skills.json'
        test.write_text(json.dumps({'skill': 'building-skills', 'threshold': 0.5,
                                    'should_trigger': ['make a skill'], 'should_not_trigger': ['fix a test']}))
        act = 'case "$1" in *skill*) echo \'{"type":"tool_use","name":"Skill","input":{"skill":"building-skills"}}\';; esac'
        with mock.patch.dict(os.environ, {'EVAL_ACT': act}):
            rows = run.run_skill(test, 'fake', 2, self.overrides, 60, {'fake': run.SKILL_SEEN['claude']})
        self.assertEqual([(r['prompt'], r['rate'], r['status']) for r in rows],
                         [('make a skill', 1.0, 'pass'), ('fix a test', 0.0, 'pass')])


class TestCommandLine(Fake):
    def call(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                code = run.main(list(args))
            except SystemExit as error:
                code = int(error.code or 0)
        return code, out.getvalue()

    def test_check_validates_and_counts(self) -> None:
        code, out = self.call('--check')
        self.assertEqual(code, 0, out)
        self.assertIn(f'scenarios cover {len(run.rule_ids())} rules', out)
        self.assertIn(f'prompt scenarios cover {len(run.universal())} universal prompts', out)

    def test_a_dry_run_of_the_prompts_counts_both_conditions(self) -> None:
        code, out = self.call('--apps', 'claude', '--prompts', '--dry-run')
        self.assertEqual(code, 0, out)
        self.assertIn(f'Would run {2 * len(run.load_prompt_scenarios())} model calls', out)
        code, out = self.call('--apps', 'claude', '--prompts', 'fix-a-bug', '--runs', '3', '--dry-run')
        self.assertIn('fix-a-bug-root-cause', out)
        self.assertIn('Would run 6 model calls', out)

    def test_an_unknown_prompt_scenario_is_refused(self) -> None:
        code, out = self.call('--apps', 'claude', '--prompts', 'make-coffee', '--dry-run')
        self.assertEqual(code, 2, out)
        self.assertIn('no prompt scenario named make-coffee', out)

    def test_the_prompt_summary_names_the_hurried_request(self) -> None:
        rows = [{'scenario': 'fix-a-bug-root-cause', 'app': 'fake', 'condition': condition, 'status': status}
                for condition, status in (('with', 'pass'), ('without', 'fail'))]
        table = run.summary(rows, ('With the prompt', 'The hurried request'))
        self.assertIn('| Scenario | App | With the prompt | The hurried request | Difference |', table)
        self.assertIn('| fix-a-bug-root-cause | fake | 1/1 | 0/1 | +100% |', table)

    def test_a_dry_run_calls_nothing(self) -> None:
        code, out = self.call('--apps', 'claude', '--rules', 'OPS-001', '--dry-run')
        self.assertEqual(code, 0, out)
        self.assertIn('Would run 4 model calls', out)

    def test_an_app_without_a_command_is_refused(self) -> None:
        code, out = self.call('--apps', 'grok', '--dry-run')
        self.assertEqual(code, 2, out)
        self.assertIn('give one with --command', out)


if __name__ == '__main__':
    unittest.main(verbosity=2)
