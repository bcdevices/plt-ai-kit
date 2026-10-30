---
name: plt
description: >-
  Reference for PLT (Production Line Tool) manufacturing test systems by Blue Clover Devices — every test plan command with its arguments and limits, PLT-106/200A/300A hardware, probes and signals, programming targets, and peripherals. Use when the user asks what a PLT command or argument does, which hardware, target or peripheral is supported, or mentions PLT, a DUT fixture, ICT or finished-goods test. For PLTcloud use plt-cloud; to write or edit a test plan use plt-test-plan-builder; to diagnose a failing step use plt-debugging.
metadata:
  version: "20261030.0.4"
---

# PLT — Production Line Tool

PLT is a family of benchtop test and programming instruments from Blue Clover
Devices. A PLT sits on an electronics production line, runs automated tests
against a device under test (DUT), programs its firmware, and
reports results to PLTcloud.

Current generation products:

- **PLT-106** — compact, current generation model. The PLT-106 is supported by
  additional BCD devices:
  - **Test Agent (PER-101)** — USB-attached Single Board Computer running
    agentOS. A plan sends it files with `agentCfg` and runs shell commands
    on it with `agentExec`.
  - **Flashr (PER-401)** — USB CMSIS-DAP (SWD) programmer running flashOS,
    attached to a Test Agent. This is the main way to program a DUT: run
    `flashr-flash` with `agentExec`, not the `program` command.

Previous generations
- **PLT-300A** — Added the multiplexer sub-system, DMM-based measurement,
  continuous measurement, and per-ground measurement.
  Some commands and channels are PLT-300A-only.
- **PLT-200A** — previous generation.

## Commands

45 commands are available, grouped into
`references/commands/` — one file per group so only the group you need
enters context. This list is the index: find the command, then open the
group file named beside its group.

In the group files' argument tables a `<placeholder>` is a value you supply
and a bare name is a literal keyword, matching the usage line. Each
command's documentation page is `TestPlanReference/command/<name>/`, with a
space in a two-word name written as an underscore (`usb_storage`).

**Programming and identification** — `references/commands/programming.md`
- `erase` — Erase DUT Flash (2 forms)
- `identify` — Identify DUT
- `program` — Program DUT (3 forms)

**Measurement** — `references/commands/measurement.md`
- `eval` — Evaluate Expression
- `freq` — Frequency Monitor Control
- `measure` — Probe Measurement (2 forms)
- `value` — Parse values

**Digital I/O and signal routing** — `references/commands/digital-io.md`
- `mux` — Multiplex Control
- `pin` — Digital pin control
- `short` — Connect Multiplex channels

**Power and ground** — `references/commands/power.md`
- `ground` — Ground Selection
- `power` — Power Control

**UART and serial** — `references/commands/serial.md`
- `ftdiCfg` — Configure external FTDI [Deprecated]
- `uart` — Send and Extract UART response
- `uartAwait` — Await UART response
- `uartBreak` — Control UART Break
- `uartCfg` — Configure UART (2 forms)
- `uartExpect` — Set expectation for uartAwait
- `uartReadTimeout` — Test if UART is not transmitting

**CAN bus** — `references/commands/can.md`
- `canCfg` — Configure CAN interface
- `canClear` — Clear CAN Buffer
- `canMatch` — Match received CAN message
- `canSend` — Send CAN message

**BLE** — `references/commands/ble.md`
- `ble gatt` — GATT-level BLE Tests
- `ble test` — Low-level BLE Tests
- `bledis` — Test BLE Discovery

**NFC** — `references/commands/nfc.md`
- `nfc` — NFC Interaction (2 forms)

**USB** — `references/commands/usb.md`
- `usb detect` — USB Device Detection
- `usb power` — USB Port Power Control
- `usb reset` — USB Reset
- `usb storage` — USB Storage (3 forms)

**External instruments** — `references/commands/instrument.md`
- `scpi` — SCPI Interaction (3 forms)

**Operator interaction** — `references/commands/operator-ui.md`
- `image` — Set background image
- `label` — Set Label Substitutions
- `operator` — Operator Test
- `scan` — Scan Barcode

**Keys and data capture** — `references/commands/data.md`
- `define` — Define user key
- `store` — Store file to Report Connector

**Flow control** — `references/commands/control.md`
- `resume` — Control resume behavior
- `sleepms` — Delay [Deprecated]
- `wait` — Delay

**Test Agent** — `references/commands/agent.md`
- `agentCfg` — Configure Agent (2 forms)
- `agentExec` — Execute command on Agent

**PLTcloud** — `references/commands/cloud.md`
- `serial` — Request or set serial number
- `webhook` — Invoke webhook

## Where to look

| Need | Read |
|---|---|
| Which group a command is in | The command list above |
| Full syntax and arguments for a command | `references/commands/<group>.md` |
| Programming a DUT through a Flashr (`flashr-flash`, `flashr-update`, OpenOCD, pyOCD) | `references/flashr.md` |
| Test Agent setup; the tools and environment agentOS gives `agentExec` | `references/test-agent.md` |
| Which `target` names `program`, `erase` and `identify` accept (the PLT's built-in programming interfaces), and every target documentation page | `references/targets.md` |
| Top-level plan keys and step fields | the `plt-test-plan-builder` skill's `references/test.plan-2.7.0.schema.json` (JSON Schema) |
| How-to guides for measurement, UART, CAN, BLE, NFC, USB, operator, fixture; plan YAML and keys; design for test | the `plt-test-plan-builder` skill's `references/` |
| A specific peripheral or sample project | `references/hardware-catalog.md` |
| Board-specific wiring, jumpers, or programming-interface setup for a dev kit | `https://docs.pltcloud.com/samples/board/<board>.html` (fetch) |
| PLTcloud: web console, releases and deployment, webhooks, CI upload, reports | the `plt-cloud` skill |
| Uploading and running a test plan from the command line | the `pltutil` skill |

Load only the group file you need. Each command has a stable
`## <name>` heading within its group file.

## Test Plans

Test plans are yaml files with a particular structure. For information on
creating test plans, see the `plt-test-plan-builder` skill.

## Full documentation

The complete reference is published at https://docs.pltcloud.com/. When the question goes beyond what is
bundled here, point the user at that URL rather than guessing.

Page paths in this skill and its references are relative to https://docs.pltcloud.com/ — a page's URL is that base plus its path.

These parts of the documentation are not bundled in any skill; fetch the
page (path relative to https://docs.pltcloud.com/) when a question needs it:

- PLT-300A and PLT-200A hardware references — `plt-300a/`, `plt-200a/`
- PLT-106 overview — `plt-106/`
- Probes and signals: PLT-200A/300A rails and test probes — `design/signals/`
- Release notes for pltOS, agentOS and flashOS — `releases/`
- Product policies (end-of-life, update patches) — `policies/`

Dev-kit documentation — pinouts, jumper positions, ST-Link / SWD / DFU
wiring and boot-mode instructions for each supported board — lives at
https://docs.pltcloud.com/samples/board/ (one page per board, e.g.
`https://docs.pltcloud.com/samples/board/nucleo_h753zi.html`). Fetch that page when the
user asks how to physically wire, jumper or bring up a specific dev kit;
none of it is bundled here.
