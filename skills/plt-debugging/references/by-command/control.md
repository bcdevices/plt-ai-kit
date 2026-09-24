# Flow control — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/control.md`.

## sleepms

> **NOTE:** If duration cannot be parsed as an integer, it is instead treated as message (i.e. sleepms <message> with no explicit duration), and a timeout: step field must supply the delay.
