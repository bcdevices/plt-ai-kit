# Keys and data capture — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/data.md`.

## store

> **NOTE:** The step fails if key is not set, or if it does not hold a valid file reference.

> **NOTE:** Earlier versions called the positional argument <memHandle>. The name changed to <key> to reflect that it is an ordinary user key (populated by an earlier step's extractKey:), not a distinct handle type. The command syntax and behavior are unchanged — existing test plans that pass a file-reference key continue to work.
