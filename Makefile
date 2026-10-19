# The hub's commands. Each one is plain Python from the standard library, so
# the same targets run on a Mac, in CI and in a cloud session. The one
# exception is PyYAML, which the repository validator in `make lint` needs and
# `make setup` installs. `make help` lists them.

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

lint: ## The repository validator, every rendered copy checked against its source, and the evals
	$(PYTHON) .github/scripts/validate-repository.py
	$(PYTHON) scripts/render.py --check
	$(PYTHON) evals/run.py --check

test: ## Every test in the repository
	$(PYTHON) -m unittest discover -s .github/scripts -p 'test_*.py'
	$(PYTHON) -m unittest discover -s scripts -p 'test_*.py'
	$(PYTHON) -m unittest discover -s probe -p 'test_*.py'
	$(PYTHON) -m unittest discover -s setup -p 'test_*.py'
	$(PYTHON) -m unittest discover -s evals -p 'test_*.py'

render: ## Rewrite every copy from CONSTITUTION.md, and the kit from its sources
	$(PYTHON) scripts/render.py --write

probe: ## Prove which files each installed app loads, one model call per check
	$(PYTHON) probe/loader-probe.py $(ARGS)

evals: ## Measure each rule with the block and without; ARGS='--apps claude --dry-run'
	$(PYTHON) evals/run.py $(ARGS)

audit: ## Report what every repository carries, against the latest release
	$(PYTHON) scripts/sync.py audit $(ARGS)

sync: ## Open or update one pull request per repository; ARGS=--dry-run previews
	$(PYTHON) scripts/sync.py sync $(ARGS)

merge: ## Merge every green sync pull request whose diff is only the block, starting checks that wait
	$(PYTHON) scripts/sync.py merge $(ARGS)

pins: ## The hashes to pin for VERSION, or for this checkout
	$(PYTHON) scripts/render.py --pins $(VERSION)

cloud-setup: ## The Claude cloud setup script, pinned to VERSION
	@test -n "$(VERSION)" || { echo 'usage: make cloud-setup VERSION=vX.Y.Z' >&2; exit 2; }
	@$(PYTHON) scripts/render.py --setup $(VERSION)
