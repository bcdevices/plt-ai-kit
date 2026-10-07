# plt-lint: offline validator for PLT test-plan YAML
#
# Common developer targets. All commands run from tools/plt-lint/.

PY ?= python3

# The linter and its catalog ship inside the plt-test-plan-builder skill.
SCRIPTS := ../../skills/plt-test-plan-builder/scripts

.PHONY: help test lint install-dev clean

help:
	@echo "targets:"
	@echo "  test            run linter unit tests"
	@echo "  lint FILE=<f>   lint a single YAML file (FILE=path.yaml)"
	@echo "  install-dev     pip install pyyaml (only runtime dep)"

test:
	$(PY) -m unittest discover -s tests -v

lint:
	$(PY) $(SCRIPTS)/plt_lint.py $(FILE)

install-dev:
	$(PY) -m pip install pyyaml

clean:
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
