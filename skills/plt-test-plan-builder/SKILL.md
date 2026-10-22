---
name: plt-test-plan-builder
description: >-
  Create or modify Blue Clover Devices' PLT (Production Line Tool) test plans in YAML for Blue Clover. Use when writing or editing a test plan, structuring test steps, or when the user asks how to test a board, program a target, or measure a signal with a PLT. For command syntax detail and hardware limits it defers to the plt skill; for a failing step use plt-debugging.
metadata:
  version: "20261022.0.1"
---

# Building PLT Test Plans

A test plan is a YAML file that a Production Line Tool runs to program and/or
test a device under test (DUT).

## The shape of a plan

A plan has a `title:` and a `suite:` of test items. Each item has an `ident:`,
a `title:`, and `steps:`. Each step runs one `command:`.

```yaml
title: "Program DUT with Flashr"
suite:
  - ident: DEV-T1
    title: Setup Test Agent
    steps:
      - command: agentCfg AGENT
        with:
          - firmware.hex

  - ident: DEV-T2
    title: Program DUT
    steps:
      - command: agentExec AGENT "flashr-flash nrf52 /run/pltagent/mnt/firmware.hex"
        timeout: 2m
        fail: "Check SWD wiring and target power"
```

All items must pass for the plan to pass; a step fails the item if its
command fails.

### Step fields worth knowing

| Field | Use |
|---|---|
| `title:` | Operator-facing description of the step. |
| `fail:` | Message shown when the step fails; make it actionable. |
| `retry:` | Retry the step (or item) N times before failing. |
| `timeout:` | Time limit, as `400ms`, `5s`, `1m`. |
| `extractKey:` | Store a command's result under a key for later reuse. |
| `if:` | Run the step (or item) only when an expression is true. |

The full envelope — every top-level key, item field, and step field — is
defined by the JSON Schema, `references/test.plan-2.7.0.schema.json`.

## Programming the DUT

The main pattern is a Test Agent (PER-101) with a Flashr (PER-401), as
above: `agentCfg` sends the image to the agent (`with:` files appear in
`/run/pltagent/mnt`), then `agentExec` runs `flashr-flash <target>
<firmwareFile> [<offset>]` there.

- `<target>` is an OpenOCD target name (`nrf52`, `stm32f4x`), not a PLT
  `program` target.
- A `.bin` image needs the flash address as `<offset>`; `.hex` and `.elf`
  must not have one.
- Always set `timeout:`; the `agentExec` default is 1000 ms.
- `flashr-flash` writes, verifies and resets, and a failure fails the step,
  so no separate identify or erase step is needed.

Details are in `examples/programming.md`; other tools on the agent are in
the `plt` skill's `references/test-agent.md`.

`identify` / `erase` / `program` drive the PLT's built-in programming
interfaces instead; use them only when the station programs that way
(`examples/suite-nucleo_f401re-blinky.yaml`).

## How to author a plan

1. **Start from an example in the `examples/` directory.**
2. **Program the DUT first.** Almost every plan begins by programming
   firmware; see "Programming the DUT" above. Get that working before
   adding tests.
3. Identify the commands needed. Look in the `plt` skill's `references/commands/`
   group files, which list every group and command with full syntax,
   arguments, notes, and warnings.
4. **Give every step a `title:` and, if relevant, a meaningful `fail:`.**
   Both surface to the operator and in the report.
   A `fail:` should say what to do, not just that it
   failed — "check for D1 solder defect" beats "measurement failed".
5. **Order steps cheapest and most diagnostic first.** An item fails at its
   first failing step, so safety checks before power, and a quick sanity
   measurement before a long functional test.
6. **Start acceptance ranges generous.** Tighten them once there is data from
   real units.
7. **Lint.** Run plt-lint on the plan and fix every finding. See
   "Validating a plan" below.

## Common patterns

**Retries.** `retry:` on an item retries the whole item; on a step, just that
step. Use it for a flaky discovery or a measurement that occasionally needs a
second attempt.

```yaml
- ident: BLE-1
  title: "Discover DUT over BLE"
  retry: 3
  steps:
    - command: bledis %BLEMAC% 30
```

**Timeouts.** `timeout:` takes a unit suffix (`400ms`, `5s`, `1m`); a bare
number is milliseconds. Set it on a step that can hang, such as an operator
prompt or a UART await.

```yaml
- command: operator "Confirm the LED is lit"
  timeout: 30s
```

**Keys.** `extractKey:` stores a command's result under a key; `define` sets
one directly, for constants the plan reuses. Reference either as `%KEY%`.

```yaml
- ident: ID-1
  title: "Scan the MAC and program firmware"
  steps:
    - command: scan ANY
      extractKey: MAC_ADDRESS
    - command: define FIRMWARE ly10-demo-fw-0.1.8.hex
    - command: program nRF52 %FIRMWARE%
    - command: label keys MAC_ADDRESS
```

**Conditional execution.** `if:` takes an expression over keys, written bare
(no `%`): `true`, `numeric(A) > 1`, `A == 'enabled'`. On an item it skips the
whole item; on a step, just that step.

```yaml
- title: "Optional BLE test"
  if: "BLE_FITTED == 'yes'"
  steps:
    - command: bledis %BLEMAC% 30
```

**Teardown.** Steps under a top-level `teardown:` run after the suite
finishes, whether it passed, failed or was aborted by the operator. Teardown
stops at its first failing step, so put power-down steps first.

```yaml
title: "Plan with teardown"
suite:
  - ident: T1
    steps:
      - command: power 3V3 on
      # ... tests ...
teardown:
  steps:
    - command: power off
```

## Validating a plan

Lint every plan you write or edit with **plt-lint** before handing it back,
and fix what it reports. It is found in `scripts/plt_lint.py`, next to its
command catalog.

```
python3 <skill-dir>/scripts/plt_lint.py --strict <plan>.yaml
```

- Exit `0` is clean; `1` means errors were reported. Exit `3` means PyYAML is
  missing — `python3 -m pip install pyyaml`.
- `--json` emits machine-readable findings when you need to process them.
- Treat warnings as defects to fix or to explain to the user, not noise.

plt-lint does not check that images referenced by `program`/`download` exist,
that `if:` expressions evaluate, or anything that needs a real DUT — a clean
lint is not a passing run.

If plt-lint cannot run (no `python3`, or PyYAML cannot be installed), say so
and fall back to the bundled JSON Schema at
`references/test.plan-2.7.0.schema.json` (schema version
2.7.0) with any JSON Schema validator, plus `yamllint`.

### Manual Review

- **Check power safety before applying power.** See
   `references/electrical-safety.md`. A short circuit or an out-of-range voltage
   can damage the PLT or the DUT. Flag any concerns you cannot verify yourself.

## Reference guides

The Test Plan Reference topic pages and design-for-test guidance are
bundled from the documentation. Each page is a `## <title>` section.

| Need | Read |
|---|---|
| Plan YAML definition, keys and `%KEY%` substitution | `references/plan-yaml.md` |
| Measuring voltage, current, resistance, frequency | `references/measurement.md` |
| Safety checks before applying power | `references/electrical-safety.md` |
| Power rails, digital pins, mux routing and shorts, ground select | `references/fixture-control.md` |
| Operator prompts, barcode scanning, label printing | `references/operator-interaction.md` |
| Serial numbers from PLTcloud or a webhook, or set from a scan | `references/cloud-interaction.md` |
| What to test; links to board, firmware and PPC design for test | `references/design-for-test.md` |

## Examples in this skill

See `examples/README.md`: full plans with the commands each uses, and
snippets per interface (programming, UART, CAN, BLE, NFC, USB).

## Full documentation

The complete Test Plan Reference is at
https://docs.pltcloud.com/TestPlanReference/

Page paths in this skill and its references are relative to https://docs.pltcloud.com/ — a page's URL is that base plus its path.
