# Blue Clover Devices Agent Toolkit

This repository contains agent skills, MCP server specs, supporting tooling, and plugin information for using coding and chat agents to drive Blue Clover Devices systems.

This repository is structured as a **Claude Code plugin** and can be installed directly.

## Install

The plt-lint tool bundled with the plt-test-plan-builder skill requires `python3` with PyYAML:

```
python3 -m pip install pyyaml
```

Add this repository as a marketplace in Claude Code, then install the plugin:

```
/plugin marketplace add bcdevices/plt-agent-kit
/plugin install plt-agent-kit@plt-agent-kit
```

Or, if you're using a local checkout:

```
/plugin marketplace add /path/to/plt-agent-kit
/plugin install plt-agent-kit@plt-agent-kit
```

## Update

Refresh the marketplace, then update the plugin and restart Claude Code:

```
/plugin marketplace update plt-agent-kit
/plugin update plt-agent-kit@plt-agent-kit
```
