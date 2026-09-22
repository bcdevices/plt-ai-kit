# plt-lint

Linter for PLT (Production Line Tool) test-plan YAML files.

## What it checks

For every step in `setup`, `panel-setup`, `trigger`, `suite`,
`teardown`, and `panel-teardown`:

1. **Top-level structure** - required fields (`suite`), known fields
   (`title`, `dutProduct`, `runs-on`, …).
2. **Step fields** — unknown keys (e.g. `timout:` for `timeout:`) as
   warnings by default, errors under `--strict`.
3. **`timeout:` format** — accepts `"200ms"`, `"5s"`, `"1m30s"`,
   integer milliseconds, or a bare decimal (`"1.5"` → 1.5 ms).
4. **Command name** - matches an actual PLT command
5. **`MinArgs`** — command has enough positional arguments after the
   tokenizer runs.
6. **Argument types** — CAN ports (`CAN0`, `CAN1`, …), UART ports
   (`UART0`, `UART1`, …), power rails (`3V3`, `VARV`, …), agent /
   SCPI / storage handle name rules, hex payload bytes in `int8`
   range, integer ranges, etc.
7. **Sub-command dispatch** — for commands like `ble gatt <sub>`,
   `usb storage <sub>`, `scpi query|command`, `serial request|set`.
8. **Enum arguments** — `resume on|off`, `pin ... input|output`,
   `short ... set|release`.
9. **Required step fields** — `wait` needs `timeout:`; `agentFetch`
   needs `with:`.
10. **Ignored step fields** — warn when a command declares a step field
   but does not use it(e.g. `id:` on `uartCfg`), since the runtime
   silently discards it.

Every check that names a specific command is driven by `plt_command_catalog.json`.

### Argument type reference

| type | validator |
|---|---|
| `canPort` | must match `CAN\d+` |
| `uartPort` | `UART0`/`UART1` on standard PLT-106; `UART\d+` accepted for extended setups |
| `agentHandle` / `scpiHandle` / `storageHandle` | non-empty, no `./:` or whitespace |
| `powerRailOrOff` | one of the enumerated power rails, or `off` |
| `uartBreakState` | `on`, `off`, or positive integer milliseconds |
| `uartSpeedOrTp` | `tp`, or positive integer bitrate |
| `hexByte` | integer parseable via Go `ParseInt(s, 0, 8)`, i.e. `-128..127` |
| `groundRange` | `none`, `all`, or a comma-separated list of `1..4` or ranges |
| `int` / `int16` / `int32` / `uint` / `uint32` | numeric literal (accepts `0x`, `0o`, `0b`) |
| `string` | any value |

Unknown types fall through as `string` (no check).

## What it does NOT check

- Whether images referenced by `program` / `download` exist.
- Whether YubiKey / PLTcloud state is compatible.
- Whether `if:` expressions evaluate correctly.
- Whether a command's runtime side-effects will succeed.
- Anything that requires a real DUT or a live network.

## Setup

```
make install-dev            # installs PyYAML, the only runtime dep
```

## Usage

Run the script directly from the source tree:

```
python3 plt_lint.py path/to/plan.yaml
python3 plt_lint.py --strict *.yaml
python3 plt_lint.py --json plan.yaml
```

Exit codes:

- `0`: success
- `1`: an error was reported
- `2`: command line invocation had an error or catalogue missing
- `3`: PyYAML isn't installed.
