PY ?= python3
MANIFESTS := .claude-plugin/plugin.json .codex-plugin/plugin.json

.PHONY: help bump check-version

help:
	@echo "targets:"
	@echo "  bump VERSION=<x.y.z>   set the plugin version in every manifest"
	@echo "  check-version          fail if the manifests disagree on the version"

bump:
	@test -n "$(VERSION)" || { echo "usage: make bump VERSION=<x.y.z>"; exit 2; }
	@perl -pi -e 's/^(\s*"version":\s*)"[^"]*"/$$1"$(VERSION)"/' $(MANIFESTS)
	@$(MAKE) --no-print-directory check-version

check-version:
	@$(PY) -c 'import json, sys; v = {f: json.load(open(f))["version"] for f in sys.argv[1:]}; [print(f"{f}: {x}") for f, x in v.items()]; sys.exit(len(set(v.values())) != 1)' $(MANIFESTS)
