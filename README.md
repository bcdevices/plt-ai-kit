# Blue Clover Devices Agent Toolkit

This repository contains agent skills, MCP server specs, supporting tooling, and plugin information for using coding and chat agents to drive Blue Clover Devices systems.

This repository is structured as a **Claude plugin** and can be installed directly in Claude Code, claude.ai and the Claude desktop app.

## Install

The plt-lint tool bundled with the plt-test-plan-builder skill requires `python3` with PyYAML:

```
python3 -m pip install pyyaml
```

### Claude Code

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

### claude.ai / Desktop

1. Open **Customize > Plugins** ([claude.ai/customize/plugins](https://claude.ai/customize/plugins)).
2. Choose **Add > Add marketplace** and enter `bcdevices/plt-agent-kit`.
3. Install the `plt-agent-kit` plugin.

The plugin is saved to your account, so it is also available in Cowork and Claude Code without installing it again. In chat, Claude loads a skill when the task matches it, or you can pick one by typing `/` in the message box.

Chat loads the plugin's skills only; `plt-lint` will be accessible in the `plt-test-plan-builder` skill.

## Update

In Claude Code, refresh the marketplace, then update the plugin and restart Claude Code:

```
/plugin marketplace update plt-agent-kit
/plugin update plt-agent-kit@plt-agent-kit
```

In claude.ai / Desktop, open **Customize > Plugins** and select **Check for updates** on the marketplace, or turn on **Sync automatically**.
