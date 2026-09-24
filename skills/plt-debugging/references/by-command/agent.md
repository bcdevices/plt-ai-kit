# Test Agent — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/agent.md`.

## agentCfg

> **NOTE:** These bare id: forms are the older way of identifying an agent, used on a PLT-200A and by test plans written before the prefixed Agent ID formats above were added. They are still parsed heuristically (see the (bare) rows in that table) and continue to work on a PLT-200A, but new test plans should prefer the prefixed vid:/mac: forms, since the bare heuristics can be ambiguous.

> **NOTE:** For Ethernet-based control, the PLT agent package should be installed on the Agent PC. pypltagent-0.1.4.noarch.deb
