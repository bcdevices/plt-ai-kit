# Power and ground — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/power.md`.

## ground

> **NOTE:** Ground selection is only supported on PLT-300A, not on PLT-200A.

## power

> **NOTE:** level is only meaningful when turning a rail on. If level is omitted (or 0), SWD and JTAG are turned on without changing their currently selected voltage level, and VARV is turned on at its previously configured voltage.
