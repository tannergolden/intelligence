<!--
title: '🔬 REPOSITORY SCRIPTS'
description: 'The checks this repository runs on its own configuration, and the tests that guard them.'
type: index
-->

<div align="center">

# 🔬 REPOSITORY SCRIPTS

<a name="top"></a>

**The checks a new repository runs before it has any code of its own.**

_The first gates you have, every one under test._

</div>

---

## 💡 What This Folder Is For

A new repository has no source code to lint, but it already has configuration
that decides how it behaves: workflows, Dependabot, forms, editor settings. A
typo in any of them breaks something quietly. The scripts here check those files
from the first commit, and the tests beside them check the scripts.

They live under `.github/` so the root of the repository stays yours. Each needs
only Python 3, plus the one package pinned in
[`requirements.txt`](requirements.txt), PyYAML, for the ones that read YAML.

[`hooks/`](hooks/README.md) holds the git hooks that run the commit-message,
sign-off and secret checks on your machine before a commit exists, so a pull
request is not the first place you hear about them.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                                          | Purpose                                                                                                        |
| :------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------- |
| [`hooks/`](hooks/README.md)                                    | The git hooks this repository ships, what each catches before a commit is recorded, and how to switch them on. |
| [`evals.py`](evals.py)                                         | Measure whether the universal rules and prompts change what agents do, each with it and without.               |
| [`faculties.py`](faculties.py)                                 | Keep the kit's copy of the faculty skills, pinned to one release of tannergolden/knowledge.                    |
| [`install.py`](install.py)                                     | Install the universal rules into every AI app's home folder, check them, and take them out.                    |
| [`kit.py`](kit.py)                                             | Render everything the home kit installs besides the rules into one bundle, `home/kit.json`.                    |
| [`loader-probe.py`](loader-probe.py)                           | Phase 0 loader probe: proves which AI coding app reads which instruction file.                                 |
| [`prompts.py`](prompts.py)                                     | Check the universal prompts the hub keeps, and give each repository a prompts page of its own.                 |
| [`README.md`](README.md)                                       | This file.                                                                                                     |
| [`render.py`](render.py)                                       | Render the universal rules from the Constitution into every copy this hub publishes.                           |
| [`requirements.txt`](requirements.txt)                         | The Python packages the scripts beside this file need, and nothing else.                                       |
| [`sync.py`](sync.py)                                           | Deliver the universal rules to every repository the owner owns, and keep them there.                           |
| [`test_cloud_setup.py`](test_cloud_setup.py)                   | Tests for the Claude cloud setup script.                                                                       |
| [`test_develop.py`](test_develop.py)                           | Tests for the develop skill's validator and packager.                                                          |
| [`test_evals.py`](test_evals.py)                               | Tests for the eval runner.                                                                                     |
| [`test_faculties.py`](test_faculties.py)                       | Tests for the faculty copier.                                                                                  |
| [`test_gitignore.py`](test_gitignore.py)                       | Tests for this repository's .gitignore.                                                                        |
| [`test_guard.py`](test_guard.py)                               | Tests for the guard hook.                                                                                      |
| [`test_hooks.py`](test_hooks.py)                               | Tests for the git hooks in .github/scripts/hooks/.                                                             |
| [`test_install.py`](test_install.py)                           | Tests for the home kit installer.                                                                              |
| [`test_kit.py`](test_kit.py)                                   | Tests for the kit renderer.                                                                                    |
| [`test_loader_probe.py`](test_loader_probe.py)                 | Tests for the loader probe.                                                                                    |
| [`test_prompts.py`](test_prompts.py)                           | Tests for the universal prompts the hub keeps, and the page each repository gets.                              |
| [`test_render.py`](test_render.py)                             | Tests for the Constitution renderer.                                                                           |
| [`test_stub.py`](test_stub.py)                                 | Tests for the stub a repository carries, and the workflow and action it calls.                                 |
| [`test_sync.py`](test_sync.py)                                 | Tests for repository sync, audit, merge and apply.                                                             |
| [`test_validate_repository.py`](test_validate_repository.py)   | Tests for the repository validator.                                                                            |
| [`test_verify_stub_ceilings.py`](test_verify_stub_ceilings.py) | Tests for the stub ceiling checker.                                                                            |
| [`validate-repository.py`](validate-repository.py)             | Validate this repository's own configuration.                                                                  |
| [`verify-stub-ceilings.py`](verify-stub-ceilings.py)           | Check every stub's permission ceiling against the workflow it calls.                                           |

<!-- AUTO-INDEX:END -->

🗂️ Machined Indexes redraws this log after every push to the default branch,
from each docstring. Who runs them:

- `checks.yml` runs `validate-repository.py` as the `ci` job's `lint-command`,
  and every `test_*.py` here as its `test-command`. That discovers a test
  added beside a new script without anyone remembering to list it.
- `verify-stubs.yml` installs `requirements.txt` and runs
  `verify-stub-ceilings.py`.
- `cut-release.yml` runs `validate-repository.py` before it tags a release, so
  a release the validator fails is refused. In the template, that includes a
  change to the owner's half of `docs/Prompts.md`.
- Git runs the hooks in `hooks/` once `core.hooksPath` points at them, which
  the development container does for you; `test_hooks.py` holds them to the
  same rules CI applies.

> [!NOTE]
> **The tests keep their underscores on purpose.** `unittest` imports each
> `test_*.py` as a module, and a module name cannot contain a hyphen, which is
> the one exception the naming standard allows. The scripts are run as files,
> so their names are hyphenated like everything else.

---

## 🚀 Running Them Locally

From the root of the repository:

```bash
python3 -m pip install --require-hashes --requirement .github/scripts/requirements.txt
python3 .github/scripts/validate-repository.py
python3 -m unittest discover -s .github/scripts -p 'test_*.py'
```

And once per clone, to have git run the hooks:

```bash
git config core.hooksPath .github/scripts/hooks
```

`verify-stub-ceilings.py` also needs the standards checked out at `v1` in
`.standards/`, which `verify-stubs.yml` does before it runs it.

Once `lint-command` points at your project's real linter, the validator can stay
as a second gate or go. What it checks stays true either way.

---

<div align="center">

**Configuration checked from the first commit, and the checkers checked too.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
