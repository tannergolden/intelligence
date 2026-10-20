# The hub's commands. Each one is plain Python from the standard library, so
# the same targets run on a Mac, in CI and in a cloud session. The one
# exception is PyYAML, which the repository validator in `make lint` needs and
# `make setup` installs. Every script they run lives in .github/scripts/,
# beside its test. `make help` lists them.

SCRIPTS := .github/scripts

PYTHON ?= python3
PYYAML_VERSION ?= 6.0.3
ARGS ?=
VERSION ?=

# Every target is phony. For setup it matters: make would otherwise take the
# setup/ folder beside this file for that target, already built, and skip it.
.PHONY: help setup check lint test render probe evals audit sync merge pins cloud-setup

help: ## List every target
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed -E 's/:.*## /|/' | awk -F '|' '{ printf "  %-12s %s\n", $$1, $$2 }'

setup: ## Install PyYAML, which the repository validator needs; CI runs this first
	$(PYTHON) -m pip install --quiet "pyyaml==$(PYYAML_VERSION)"

check: lint test ## Everything CI checks

lint: ## The repository validator, every rendered copy checked against its source, the prompts, and the evals
	$(PYTHON) $(SCRIPTS)/validate-repository.py
	$(PYTHON) $(SCRIPTS)/render.py --check
	$(PYTHON) $(SCRIPTS)/prompts.py --check
	$(PYTHON) $(SCRIPTS)/evals.py --check

test: ## Every test in the repository
	$(PYTHON) -m unittest discover -s $(SCRIPTS) -p 'test_*.py'

render: ## Rewrite home/ from CONSTITUTION.md, the kit and the installer
	$(PYTHON) $(SCRIPTS)/render.py --write

probe: ## Prove which files each installed app loads, one model call per check
	$(PYTHON) $(SCRIPTS)/loader-probe.py $(ARGS)

evals: ## Measure each rule and universal prompt, with it and without; ARGS='--apps claude --dry-run'
	$(PYTHON) $(SCRIPTS)/evals.py $(ARGS)

audit: ## Report what every repository carries, against the latest release
	$(PYTHON) $(SCRIPTS)/sync.py audit $(ARGS)

sync: ## Open or update one pull request per repository; ARGS=--dry-run previews
	$(PYTHON) $(SCRIPTS)/sync.py sync $(ARGS)

merge: ## Merge every green sync pull request whose diff is only the block, starting checks that wait
	$(PYTHON) $(SCRIPTS)/sync.py merge $(ARGS)

pins: ## The hashes to pin for VERSION, or for this checkout
	$(PYTHON) $(SCRIPTS)/render.py --pins $(VERSION)

cloud-setup: ## The Claude cloud setup script, pinned to VERSION
	@test -n "$(VERSION)" || { echo 'usage: make cloud-setup VERSION=vX.Y.Z' >&2; exit 2; }
	@$(PYTHON) $(SCRIPTS)/render.py --setup $(VERSION)
