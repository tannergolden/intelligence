# =============================================================================
# Makefile - the standardized task entry point
# =============================================================================
# The shared CI workflow resolves each stage in one order: the command passed
# from the calling stub, else `make <stage>`, else skip. Documentation is the
# exception and has NO input override, so `lint-docs` resolves from this file
# or does not run at all.
#
# That is why this file exists rather than four inputs in ci.yml: it is the
# only way the documentation gate runs, and it makes the same checks available
# locally under the same names CI uses. A gate you cannot run before pushing
# is a gate that teaches you things too late.
#
# No dependencies, deliberately. Both checkers are standard library only, so
# `setup` has nothing to install and says so rather than pretending.
# =============================================================================

.DEFAULT_GOAL := help
.PHONY: help setup lint lint-docs test build clean

PYTHON ?= python3
SKILLS := skills/.unpackaged
DIST := dist
PACKAGER := $(SKILLS)/develop/scripts/package.py

help: ## Show every target and what it does
	@echo "Targets:"
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[1m%-12s\033[0m %s\n", $$1, $$2}'

setup: ## Verify the toolchain (nothing to install: both checkers are stdlib only)
	@$(PYTHON) --version
	@echo "Nothing to install. Both checkers use the standard library only."

lint: ## Check every published skill against the Agent Skills specification
	$(PYTHON) .github/actions/check-skills/check-skills.py $(SKILLS)

lint-docs: ## Audit every document against the published styling standard
	$(PYTHON) scripts/check-docs.py .

test: ## Prove both checkers still reject known-bad input
	$(PYTHON) .github/actions/check-skills/check-skills.py --self-test
	$(PYTHON) scripts/check-docs.py --self-test

build: ## Package every skill into $(DIST)/ as an installable archive
	@mkdir -p $(DIST)
	@for skill in $(SKILLS)/*/; do \
		[ -f "$$skill/SKILL.md" ] || continue; \
		$(PYTHON) $(PACKAGER) "$$skill" --out $(DIST); \
	done

clean: ## Remove build output
	rm -rf $(DIST)
