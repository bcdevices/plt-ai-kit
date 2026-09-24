---
name: plt-debugging
description: >-
  Diagnose failures when running PLT (Production Line Tool) test plans on Blue Clover Devices hardware — measurement, programming, UART, CAN and power steps that fail or behave unexpectedly. Use when a PLT test step fails, a plan behaves unexpectedly, or the user asks why a PLT measurement or programming operation is not working. Not for writing a new plan (plt-test-plan-builder) or looking up what a command does (plt).
metadata:
  version: "20260415.0.1-21-ga5a80b0d7"
---

# Debugging PLT Test Plans

When a PLT test step fails, work from what the step reports toward a cause.
This skill collects the documented gotchas per command, a growing catalogue of
failure modes, and which features need which PLT-OS version.

## Triage

1. **Read the step's failure.** The `fail:` message, the command, and the
   reported value narrow the search immediately. A value near its range is a
   different problem from one wildly off or a timeout.
2. **Identify the subsystem** from the command that failed and open its
   gotchas file below.
3. **Check the command's documented gotchas** in the matching
   `references/by-command/<subsystem>.md`. Many failures are a note or
   warning already on the command's page — voltage limits, required
   multiplexer routing, model constraints.
4. **Insert a diagnostic step** at the failure point to narrow the cause:
   - `measure` — read a signal directly. A `measure` before a functional step
     tells you whether the problem is upstream (power, connection) or in the
     DUT.
   - `identify` — confirms the programming interface reaches the target. If
     `identify` fails, stop suspecting the firmware image.
   - `pin` (read) — read a probe's state to confirm wiring and fixture
     contact.
   - `operator` — pause the run so a person can inspect the fixture at a
     specific point.
5. **Match against known failure modes** in `references/failure-modes.md`.
6. **Rule out a version mismatch.** Get the PLT's pltOS (and agentOS)
   version, then check `references/version-gating.md` for a feature newer than
   it or a **Fixed** row matching the failure. Releases after this skill was
   built are at https://docs.pltcloud.com/releases/ . If the fix is in a newer release,
   the remedy is to update the PLT.

## By subsystem

Each file below aggregates the notes and warnings for the commands in that
subsystem; the full command syntax is in the `plt` skill's
`references/commands/<subsystem>.md` (same subsystem name). A subsystem
marked _None documented_ has no notes or warnings on its commands, so it has
no gotchas file.

| The failing step is… | Gotchas | Also |
|---|---|---|
| `measure` / `freq` / `eval` / `value` | `references/by-command/measurement.md` | Ground reference, multiplexer routing, voltage limit. |
| `program` / `identify` / `erase` | `references/by-command/programming.md` | Target power, programming interface, image path. |
| `pin` / `short` / `mux` | `references/by-command/digital-io.md` | Probe routing and short-circuit checks. |
| `power` / `ground` | `references/by-command/power.md` | Short-circuit and over-voltage checks before applying power; DUT ground selection. |
| `uart*` / `ftdiCfg` | `references/by-command/serial.md` | `uartCfg` baud and framing before suspecting the DUT. |
| `canCfg` / `canSend` / `canMatch` / `canClear` | `references/by-command/can.md` | Bitrate config and transceiver wiring. |
| `ble*` | `references/by-command/ble.md` | Advertising and GATT. |
| `nfc` | _None documented_ | NFC field. |
| `usb *` | `references/by-command/usb.md` | Enumeration, power, and storage mount. |
| `scpi` | _None documented_ | SCPI transport and reply framing. |
| `operator` / `scan` / `label` / `image` | _None documented_ | Operator flow and barcode I/O. |
| `define` / `store` | `references/by-command/data.md` | Key definition and capture. |
| `sleepms` / `wait` / `resume` | `references/by-command/control.md` | Run pacing and resume behaviour. |
| `agentCfg` / `agentExec` | `references/by-command/agent.md` | Agent connection type and agentOS version. |
| `serial` / `webhook` | _None documented_ | PLTcloud connectivity and Project Settings; see the `plt-cloud` skill. |

## Common failure modes

- **A measure step fails just outside its acceptance range** — A `measure` step fails on some units but not others. (`measurement-out-of-range`)
- **A program step fails to flash the DUT** — The `program` step fails, sometimes after `identify` succeeded, sometimes not. (`program-step-fails`)

Full symptoms, diagnosis and remedies for each are in
`references/failure-modes.md`.

## Safety first

Several failures trace back to power or connection problems, and diagnosing
them can put voltage where it should not be. Before probing or re-applying
power, follow the power-safety checks in the `plt-test-plan-builder` skill (its
electrical-safety reference). Never exceed a channel's maximum voltage — the
limit for each is with the command's warning in
`references/by-command/measurement.md` (or the matching subsystem file).

## References

| File | What it holds |
|---|---|
| `references/by-command/` | Every documented note and warning, per command, split by subsystem — one file per group, matching the `plt` skill's `references/commands/<subsystem>.md`. |
| `references/failure-modes.md` | Catalogued failure modes: symptoms, diagnosis, remedies. |
| `references/version-gating.md` | Which pltOS/agentOS version a feature needs, and which release fixed a bug. |

## Full documentation

Troubleshooting beyond what is here is supported through the PLT documentation
at https://docs.pltcloud.com/ and the PLT Support Center at
https://plt.bcdevices.com/hc/en-us .
Page paths in this skill and its references are relative to https://docs.pltcloud.com/ — a page's URL is that base plus its path.
