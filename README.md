# Blue Clover Devices Agent Toolkit

This repository contains agent skills, MCP server specs, supporting tooling, and plugin information for using coding and chat agents to drive Blue Clover Devices systems.

This repository is structured as a **Claude Code plugin** and can be installed directly.

## Install

The bundled plt-lint tool requires `python3` with PyYAML:

```
python3 -m pip install pyyaml
```

Add this repository as a marketplace in Claude Code, then install the plugin:

```
/plugin marketplace add bcdevices/bcd-agent-kit
/plugin install bcd-agent-kit@bcd-agent-kit
```

Or, if you're using a local checkout:

```
/plugin marketplace add /path/to/bcd-agent-kit
/plugin install bcd-agent-kit@bcd-agent-kit
```

## Update

Refresh the marketplace, then update the plugin and restart Claude Code:

```
/plugin marketplace update bcd-agent-kit
/plugin update bcd-agent-kit@bcd-agent-kit
```
