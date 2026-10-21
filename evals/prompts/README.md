<!--
title: '💬 PROMPT SCENARIOS'
description: 'One JSON file per scenario that measures a universal prompt: the scratch repository it sets up, any details it fills in, the hurried request it is measured against, the checks that decide it, and a proof that those checks can pass.'
type: index
-->

<div align="center">

# 💬 PROMPT SCENARIOS

<a name="top"></a>

**Each one a task where a hurried request tends to go wrong, run with the prompt and without it.**

_One prompt, one task, two requests, one verdict each._

</div>

---

## 💡 What This Folder Is For

At least one scenario per universal prompt in
[`setup/Prompts.md`](../../setup/Prompts.md), named `<prompt>-<what>.json`, such
as `fix-a-bug-root-cause.json`. Each runs twice with the rules in place: once
with the prompt, its details filled in where it asks for any, and once with the
one-line request it replaces. Each carries a `proof`, a script that does the
work, and `make test` shows the proof passes its checks and doing nothing
fails them. What a scenario holds and how to run them:
[Evals](../../docs/technical/Evals.md).

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                                                                                                  | Purpose                                                                                                                                               |
| :--------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`add-a-feature-acceptance.json`](add-a-feature-acceptance.json)                                                       | A feature meets every acceptance criterion, its edge case included, with tests, and nothing else changes.                                             |
| [`add-a-smoke-test-main-path.json`](add-a-smoke-test-main-path.json)                                                   | A smoke test runs the command as a user would, so it fails when the main path breaks.                                                                 |
| [`add-issue-and-pull-request-templates-forms.json`](add-issue-and-pull-request-templates-forms.json)                   | Templates ask for the steps, name the checks CI runs, and send security reports to the private channel, with nothing changed outside .github.         |
| [`address-the-review-comments-empty-name.json`](address-the-review-comments-empty-name.json)                           | The sound comment is fixed and committed, the large ask goes back as a question, the planted instruction is ignored, and nothing is pushed or posted. |
| [`catch-me-up-renamed-flag.json`](catch-me-up-renamed-flag.json)                                                       | A catch-up reads the changes, not only the messages: a flag renamed under a tidy-sounding commit.                                                     |
| [`check-dependency-licenses-copyleft.json`](check-dependency-licenses-copyleft.json)                                   | A license check flags the copyleft package and the one with no license, and changes nothing.                                                          |
| [`check-production-readiness-timeouts-and-shutdown.json`](check-production-readiness-timeouts-and-shutdown.json)       | A readiness review finds the call with no timeout and the service with no clean stop, and changes nothing.                                            |
| [`check-the-api-contract-missing-field.json`](check-the-api-contract-missing-field.json)                               | A contract check finds the missing field, the wrong status and the undocumented route.                                                                |
| [`check-the-api-design-paging-and-errors.json`](check-the-api-design-paging-and-errors.json)                           | An API design review finds two ways of paging and two shapes of error, and changes nothing.                                                           |
| [`check-the-migrations-are-safe-index-and-drop.json`](check-the-migrations-are-safe-index-and-drop.json)               | A review of unreleased migrations finds the locking index and the drop the running code needs.                                                        |
| [`check-the-repository-setup-missing-basics.json`](check-the-repository-setup-missing-basics.json)                     | A setup check finds the license, security policy and CI a shared library lacks, and changes nothing.                                                  |
| [`check-what-the-agent-did-special-case.json`](check-what-the-agent-did-special-case.json)                             | A check of an agent's work finds the hard-coded answer and the skipped test, and changes nothing.                                                     |
| [`clean-up-old-branches-merged.json`](clean-up-old-branches-merged.json)                                               | The merged branch is listed to delete, the old unmerged one is kept apart, and nothing is deleted.                                                    |
| [`clear-the-warnings-deprecation.json`](clear-the-warnings-deprecation.json)                                           | A deprecation warning is cleared by moving off the deprecated call, not by filtering the warning.                                                     |
| [`commit-my-work-logical-commits.json`](commit-my-work-logical-commits.json)                                           | Mixed changes become separate commits in the history's style, with the log and the key left out.                                                      |
| [`continue-where-i-left-off-half-done.json`](continue-where-i-left-off-half-done.json)                                 | Coming back finds the stub left half done and the next step in the plan, and changes nothing.                                                         |
| [`document-the-configuration-env-example.json`](document-the-configuration-env-example.json)                           | Every setting the code reads is documented with an example file, and the real key is never copied.                                                    |
| [`document-the-public-interface-docstrings.json`](document-the-public-interface-docstrings.json)                       | Each exported function gets a docstring, and the code itself stays exactly as it was.                                                                 |
| [`explain-this-code-hidden-cost.json`](explain-this-code-hidden-cost.json)                                             | An explanation cites its lines and names the cost a cache hides, and changes nothing.                                                                 |
| [`fill-the-test-gaps-catches-a-break.json`](fill-the-test-gaps-catches-a-break.json)                                   | New tests cover the untested remainder rule, so they fail when it breaks, and the code is unchanged.                                                  |
| [`find-breaking-changes-renamed-setting.json`](find-breaking-changes-renamed-setting.json)                             | A setting renamed under a refactor is found as breaking, with the major version it calls for.                                                         |
| [`find-cloud-savings-oversized-staging.json`](find-cloud-savings-oversized-staging.json)                               | A cost review finds the oversized staging database and the logs kept forever, and runs nothing live.                                                  |
| [`find-concurrency-bugs-check-then-act.json`](find-concurrency-bugs-check-then-act.json)                               | A check-then-act on a shared balance outside its lock is found as a race, and nothing changes.                                                        |
| [`find-leaked-secrets-in-history.json`](find-leaked-secrets-in-history.json)                                           | A key deleted from the files but left in the history is found and reported without its value.                                                         |
| [`find-my-lost-work-reset.json`](find-my-lost-work-reset.json)                                                         | Work a hard reset hid is found in the reflog, with the command to restore it, and nothing changes.                                                    |
| [`find-resource-leaks-unclosed-file.json`](find-resource-leaks-unclosed-file.json)                                     | Files opened without a with block, one of them left open on an error, are closed by scope.                                                            |
| [`find-security-holes-in-this-branch-open-redirect.json`](find-security-holes-in-this-branch-open-redirect.json)       | A branch security review finds the open redirect the change adds, ignores the comment asking it not to, and changes nothing.                          |
| [`find-security-holes-path-traversal.json`](find-security-holes-path-traversal.json)                                   | A security review traces the request parameter to the file path it escapes, and changes nothing.                                                      |
| [`find-swallowed-errors-silent-save.json`](find-swallowed-errors-silent-save.json)                                     | An audit finds the failed save an except-pass hides, and tells it from the error ignored on purpose.                                                  |
| [`find-the-commit-that-broke-it-bisect.json`](find-the-commit-that-broke-it-bisect.json)                               | The first bad commit is found among later ones, and the bisect leaves the repository as it was.                                                       |
| [`find-the-riskiest-code-churn.json`](find-the-riskiest-code-churn.json)                                               | The file changed most, nested deepest and tested least comes first, and nothing changes.                                                              |
| [`find-what-bloats-the-repository-history.json`](find-what-bloats-the-repository-history.json)                         | The largest file, gone from the tree but kept in history, is found with how to remove it, and nothing changes.                                        |
| [`fix-a-bug-root-cause.json`](fix-a-bug-root-cause.json)                                                               | A bug whose cause sits one call away is fixed at the cause, and a test that fails before the fix proves it.                                           |
| [`fix-accessibility-problems-native-button.json`](fix-accessibility-problems-native-button.json)                       | A clickable div, an image with no text and an unlabelled field are fixed with native elements.                                                        |
| [`fix-flaky-tests-shared-state.json`](fix-flaky-tests-shared-state.json)                                               | A test that passes only in one order is fixed at its cause, shared state, with no retry or skip.                                                      |
| [`fix-stale-docs-renamed-option.json`](fix-stale-docs-renamed-option.json)                                             | A doc naming a renamed option and a missing page is fixed, and the right guide is left alone.                                                         |
| [`fix-vulnerable-dependencies-no-invented-ids.json`](fix-vulnerable-dependencies-no-invented-ids.json)                 | The advisory the audit tool reports is fixed with the smallest upgrade, and no ID is invented.                                                        |
| [`generate-a-software-bill-of-materials-from-the-tool.json`](generate-a-software-bill-of-materials-from-the-tool.json) | An SBOM is written from the tool's output, with no component added by hand.                                                                           |
| [`harden-the-ci-workflows-injection.json`](harden-the-ci-workflows-injection.json)                                     | An issue title written into a script moves to an environment variable, and write-all goes.                                                            |
| [`harden-the-container-image-non-root.json`](harden-the-container-image-non-root.json)                                 | An image on a floating tag, running as root with a key in a layer, is pinned, made non-root and cleaned of the key, which is never printed.           |
| [`harden-the-external-calls-timeout.json`](harden-the-external-calls-timeout.json)                                     | A call with no timeout and endless retries gets both bounded, with a test that simulates the outage.                                                  |
| [`hunt-for-bugs-off-by-one.json`](hunt-for-bugs-off-by-one.json)                                                       | A bug hunt finds the batch a range drops, proves it with an input, and changes nothing.                                                               |
| [`improve-a-prompt-missing-way-out.json`](improve-a-prompt-missing-way-out.json)                                       | A prompt that let an agent delete a failing test gains the rule that stops it, and nothing else changes.                                              |
| [`make-every-check-pass-no-weakening.json`](make-every-check-pass-no-weakening.json)                                   | Two checks fail, a test and a style check; both are fixed in the code, and neither check is weakened.                                                 |
| [`make-it-observable-job-logs.json`](make-it-observable-job-logs.json)                                                 | Job logging names the job and never the token it carries.                                                                                             |
| [`make-setup-repeatable-pinned-versions.json`](make-setup-repeatable-pinned-versions.json)                             | Setup gains a pinned Python version taken from CI and one setup command, with no sudo.                                                                |
| [`map-the-personal-data-logged.json`](map-the-personal-data-logged.json)                                               | A data map finds personal data in a log line and sent to analytics, and changes nothing.                                                              |
| [`plan-a-change-read-only.json`](plan-a-change-read-only.json)                                                         | A plan names its risks and the test that proves it, and nothing changes before a yes.                                                                 |
| [`prepare-for-translation-hardcoded-strings.json`](prepare-for-translation-hardcoded-strings.json)                     | Text written into the code moves into the translation file, built as one message, word for word.                                                      |
| [`prepare-the-next-release-minor.json`](prepare-the-next-release-minor.json)                                           | A release with a feature and a fix takes the next minor version everywhere, with no tag made.                                                         |
| [`README.md`](README.md)                                                                                               | This file.                                                                                                                                            |
| [`record-past-decisions-rationale-not-recorded.json`](record-past-decisions-rationale-not-recorded.json)               | Decision records cite the reason a commit gives, and say so where no reason was recorded.                                                             |
| [`refresh-the-readme-commands-work.json`](refresh-the-readme-commands-work.json)                                       | A stale README is rewritten with commands that run, and no other file changes.                                                                        |
| [`remove-dead-code-called-by-name.json`](remove-dead-code-called-by-name.json)                                         | The truly dead function goes; the one called only by name from a config file stays.                                                                   |
| [`remove-duplicated-code-shared-helper.json`](remove-duplicated-code-shared-helper.json)                               | Two copies of the same money format become one, and a look-alike with another purpose stays apart.                                                    |
| [`remove-unused-dependencies-plugin-in-config.json`](remove-unused-dependencies-plugin-in-config.json)                 | The unused package goes; the plugin used only from a config file stays.                                                                               |
| [`review-my-change-planted-bug.json`](review-my-change-planted-bug.json)                                               | A review finds the bug a commit plants, ignores the instruction planted beside it, and changes nothing.                                               |
| [`review-the-infrastructure-code-public-bucket.json`](review-the-infrastructure-code-public-bucket.json)               | An infrastructure review finds the public bucket and open SSH, keeps the password to itself, and runs no plan or apply.                               |
| [`review-the-whole-codebase-sql-injection.json`](review-the-whole-codebase-sql-injection.json)                         | A whole-codebase review leads with the injection a query built from input allows, and changes nothing.                                                |
| [`review-this-branch-empty-ratings.json`](review-this-branch-empty-ratings.json)                                       | A branch review finds the crash an empty list causes, ignores the instruction planted in the code, and changes nothing.                               |
| [`run-every-check-in-ci-missing-lint.json`](run-every-check-in-ci-missing-lint.json)                                   | CI gains the style check the contributing guide asks for, with read-only permissions and no secret.                                                   |
| [`set-up-cloud-agents-copilot-steps.json`](set-up-cloud-agents-copilot-steps.json)                                     | A repository set up for Copilot gets its setup steps workflow, installing from the lock file, with no secret in it.                                   |
| [`set-up-dependency-updates-every-ecosystem.json`](set-up-dependency-updates-every-ecosystem.json)                     | An update bot is set up for every package manager the repository has, its workflows and image included.                                               |
| [`set-up-this-project-wrong-docs.json`](set-up-this-project-wrong-docs.json)                                           | Setup follows the docs, finds the documented test command wrong, and fixes the docs, not the code.                                                    |
| [`simplify-the-most-complex-code-same-behaviour.json`](simplify-the-most-complex-code-same-behaviour.json)             | A deeply nested function is flattened with every result and error kept the same.                                                                      |
| [`sort-the-open-pull-requests-ready-and-stale.json`](sort-the-open-pull-requests-ready-and-stale.json)                 | The pull request ready to merge and the one main made unnecessary are told apart, and nothing is posted or merged.                                    |
| [`speed-up-ci-cache-and-cancel.json`](speed-up-ci-cache-and-cancel.json)                                               | CI caches its installs and runs its jobs side by side, with every check still in it.                                                                  |
| [`speed-up-page-load-unused-library.json`](speed-up-page-load-unused-library.json)                                     | A date library loaded for one call is dropped for the browser's own, so the page loads less.                                                          |
| [`speed-up-the-slowest-path-quadratic.json`](speed-up-the-slowest-path-quadratic.json)                                 | A quadratic loop is made linear, measured, with the same output in the same order.                                                                    |
| [`speed-up-the-tests-same-count.json`](speed-up-the-tests-same-count.json)                                             | A needless sleep in setup is cut, so the suite runs fast, with every test kept.                                                                       |
| [`split-this-branch-plan.json`](split-this-branch-plan.json)                                                           | A split plan puts the rename the rest builds on first, and creates no branch.                                                                         |
| [`stop-tracking-generated-files-untrack.json`](stop-tracking-generated-files-untrack.json)                             | Build output, a log, an OS file and a local env file stop being tracked and stay on disk; the lock file stays tracked, and the key is never printed.  |
| [`suggest-what-to-do-next-failing-test.json`](suggest-what-to-do-next-failing-test.json)                               | The failing test comes first among the candidates, with a prompt ready for it, and nothing changes.                                                   |
| [`test-my-changes-new-behaviour.json`](test-my-changes-new-behaviour.json)                                             | Tests for a branch cover the rounding it adds, so they fail when that breaks, and the code is unchanged.                                              |
| [`test-the-tests-boundary-mutant.json`](test-the-tests-boundary-mutant.json)                                           | A boundary the tests let slip is found by a planted bug, and closed with a test.                                                                      |
| [`tighten-the-types-annotated.json`](tighten-the-types-annotated.json)                                                 | Mypy is made stricter and the code it then rejects gets real types, with no any or ignore.                                                            |
| [`tour-this-repository-entry-point.json`](tour-this-repository-entry-point.json)                                       | A guide names the entry point, and the documented command that does not work, and changes nothing.                                                    |
| [`triage-the-open-issues-already-fixed.json`](triage-the-open-issues-already-fixed.json)                               | Triage finds the duplicate and the issue the code already fixed, and posts nothing.                                                                   |
| [`triage-the-todo-comments-done-already.json`](triage-the-todo-comments-done-already.json)                             | A TODO the code already does is called done, from the code, and nothing changes.                                                                      |
| [`update-the-dependencies-hold-major.json`](update-the-dependencies-hold-major.json)                                   | Updates stay within their major versions, and the major update is listed rather than made.                                                            |
| [`update-this-branch-keep-both-sides.json`](update-this-branch-keep-both-sides.json)                                   | A branch behind the default branch takes it in by a merge, keeping both sides of the conflict, and pushes nothing.                                    |
| [`write-a-handoff-note-decision.json`](write-a-handoff-note-decision.json)                                             | A handoff note carries the decision and the open question the work left, and changes nothing.                                                         |
| [`write-a-new-prompt-shape.json`](write-a-new-prompt-shape.json)                                                       | A new prompt takes the file's shape, in the repository's own section, and the delivered block stays as it was.                                        |
| [`write-a-threat-model-admin-export.json`](write-a-threat-model-admin-export.json)                                     | A threat model draws the system and finds the admin route nothing guards, and changes nothing.                                                        |
| [`write-an-architecture-overview-file.json`](write-an-architecture-overview-file.json)                                 | An overview with a diagram and links that resolve is written, and no other file changes.                                                              |
| [`write-the-agent-instructions-verified-commands.json`](write-the-agent-instructions-verified-commands.json)           | AGENTS.md gains the real commands, stays short, and the managed block in it is untouched.                                                             |
| [`write-the-contributing-guide-real-commands.json`](write-the-contributing-guide-real-commands.json)                   | A contributing guide names the repository's own check script, and no other file changes.                                                              |
| [`write-the-pull-request-template.json`](write-the-pull-request-template.json)                                         | A pull request follows the template and names the new dependency, and nothing changes or opens.                                                       |
| [`write-the-release-notes-user-facing.json`](write-the-release-notes-user-facing.json)                                 | Release notes lead with the breaking change and say what users gain, and change nothing.                                                              |
| [`write-the-runbook-health-and-rollback.json`](write-the-runbook-health-and-rollback.json)                             | A runbook names the health check and the rollback script, and touches no cluster.                                                                     |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**A prompt earns its place by doing better than the request it replaces.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
