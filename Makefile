# SPDX-FileCopyrightText: 2026 Tanner Golden
# SPDX-License-Identifier: MIT
# =============================================================================
# The whole task runner. Five targets, no dependencies, nothing to install.
# =============================================================================
# There is no toolchain here on purpose: the checks are stdlib Python and the
# publishing path is Actions. `make` with no argument runs `check`, which is
# the read-only one.
#
# WHY A MAKEFILE AND NOT A SCRIPT DIRECTORY: every target below is one or two
# lines. A script per target would be five files to keep honest, and the
# checks a consumer runs live in `actions/ai-sync/` because they ship, not
# because they are convenient here.

CHECK   = actions/ai-sync/check.py
# The three always-loaded instruction files. `build` copies exactly these,
# because they are the only payload paths that have a root counterpart: the
# rest of the payload (hooks, settings, the lockfile) belongs to a CONSUMER's
# tree and would be noise, or worse, in this one.
ROUTERS = AGENTS.md CLAUDE.md GEMINI.md

.PHONY: check test build verify setup

## check: lint the payload, the bytes that will be published
check:
	python3 $(CHECK) payload

## test: prove the linter can fail, using the hostile fixtures
# A check that has never rejected anything has never been tested. The fixtures
# are written to violate the rules deliberately, so a PASS here is the
# failure: it means the suite went quiet, which is precisely the state in
# which a bad byte reaches six always-loaded instruction files unnoticed.
# `--any-path` because the fixtures are hostile INPUTS, not the emit set:
# their filenames are chosen by the rules under test, so the emitted-path
# allowlist has nothing to say about them. The hatch stays ON here, because
# one fixture asserts that the hatch itself still works.
test:
	@if python3 $(CHECK) tests/fixtures --any-path; then \
		echo "FAIL: the hostile fixtures were ACCEPTED. The checks are not working."; \
		exit 1; \
	fi
	@echo "OK: the hostile fixtures were rejected, as they must be."

## build: consume our own output, by copying the payload to the root
# This repository runs the two tools it publishes for, so its own agents must
# read exactly what a consumer reads. The root copies are GENERATED. Edit the
# ones under payload/ and run this.
build:
	@for f in $(ROUTERS); do cp "payload/$$f" "$$f"; done
	@echo "Copied $(ROUTERS) from payload/ to the repository root."

## verify: fail if the generated root copies are out of date
# Scoped to the generated paths rather than the whole tree: an unrelated edit
# in progress is not a defect, and a check that fails for the wrong reason is
# a check people learn to ignore.
verify: build
	@if [ -n "$$(git status --porcelain -- $(ROUTERS))" ]; then \
		git status --short -- $(ROUTERS); \
		echo "FAIL: the root instruction files differ from payload/. Someone edited"; \
		echo "      the generated copies, or forgot to run 'make build'."; \
		exit 1; \
	fi
	@echo "OK: the root instruction files match payload/."

## setup: install the local git hooks, once per clone
# The commit-msg hook is the ONLY commit-message enforcement here: every
# shared gate in this ecosystem is pull-request shaped, and this repository
# opens none. Git silently skips a hook that is not executable, so the chmod
# is part of the install rather than an afterthought.
setup:
	git config core.hooksPath .githooks
	chmod +x .githooks/commit-msg
	@echo "Hooks installed. Commit messages are checked before they exist."
