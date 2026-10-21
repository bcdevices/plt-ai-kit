---
name: plt-debugging
description: >-
  Diagnose failures when running PLT (Production Line Tool) test plans on Blue Clover Devices hardware — measurement, programming, UART, CAN and power steps that fail or behave unexpectedly. Use when a PLT test step fails, a plan behaves unexpectedly, or the user asks why a PLT measurement or programming operation is not working. Not for writing a new plan (plt-test-plan-builder) or looking up what a command does (plt).
metadata:
  version: "20261022.0.1"
---

# Debugging PLT Test Plans

When a PLT test step fails, work from what the step reports toward a cause.
This skill collects the documented gotchas per command, a growing catalogue of
failure modes, and which features need which PLT-OS version.

## Start from the run record, when you can

If PLTcloud tools are available in this session (`list_my_organizations`,
`list_devices`, `get_device`, `get_test_history`, `get_pass_fail_history`,
`get_device_errors`), read the failed run before asking the user to describe
it. If they are not available, skip this section and ask for the step's
`fail:` message, command and reported value instead.

1. **Find the PLT.** `list_my_organizations` gives the organization uuid;
   `list_devices` lists its PLTs by model and serial. If the user named the
   PLT, match it there rather than guessing the model or serial format.
2. **Read the failed run.** `get_test_history` for that PLT over the days in
   question returns each report's plan, result, failing step, failure detail,
   DUT serial, and the PLT app and runner versions. The failing step and
   detail are what triage step 1 asks for.
   - `INCOMPLETE` means the run never finished, including a `FAIL` with no
     failing step. Treat it as a run that stopped, not as a step that failed
     its check, and ask the user what interrupted it.
3. **Look for a pattern before a cause.** `get_pass_fail_history` gives daily
   pass, fail and incomplete counts per plan, for one PLT or the whole
   organization:
   - One DUT serial failing while others pass on the same PLT points at the
     unit.
   - Every unit failing on one PLT, while other PLTs pass the same plan,
     points at that PLT or its fixture.
   - A failure rate that starts on a particular day points at what changed
     that day: a new release, a new plan, or a PLT update.
4. **Check the PLT's own errors.** `get_device` shows the PLT's OS version,
   release and most recent error and warning summaries; `get_device_errors`
   pages through the full list. An error logged on the PLT around the time of
   the failed run is often the cause. If `errors_withheld` is true, the PLT
   has belonged to another organization and its errors can't be shown; ask
   the user to check the PLT's own logs instead.

These tools read data only. They cannot re-run a test, change a plan or
reach the PLT itself; diagnostic steps (triage step 4) are still added to
the plan and run on the PLT.

Records are clipped (failure detail at 300 characters) and windows are
capped at 90 days. If the detail you need is cut off, ask the user for the
full report from the PLTcloud web console.

## Triage

1. **Read the step's failure.** The `fail:` message, the command, and the
   reported value narrow the search immediately. A value near its range is a
   different problem from one wildly off or a timeout.
   If you read the run with the PLTcloud tools above, you already have this.
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
     `identify` fails, stop suspecting the firmware image. When programming
     through a Flashr, use the connection check in `references/flashr.md`
     instead.
   - `pin` (read) — read a probe's state to confirm wiring and fixture
     contact.
   - `operator` — pause the run so a person can inspect the fixture at a
     specific point.
5. **Match against known failure modes** in `references/failure-modes.md`.
   The PLT's own error summaries (`get_device` / `get_device_errors`) are a
   second source of known failures.
6. **Rule out a version mismatch.** Get the PLT's pltOS (and agentOS or
   flashOS) version — from `get_device` if the PLTcloud tools are available,
   otherwise from the user — then check `references/version-gating.md` for a feature newer than
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
| `agentExec` running `flashr-flash` or `flashr-update` | `references/flashr.md` | Exit status, `timeout:`, target name, image path on the agent. |
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
| `references/flashr.md` | Programming through a Test Agent and Flashr: `flashr-flash` and `flashr-update` failures by exit status, and a connection check. |
| `references/version-gating.md` | Which pltOS/agentOS/flashOS version a feature needs, and which release fixed a bug. |

## Full documentation

Troubleshooting beyond what is here is supported through the PLT documentation
at https://docs.pltcloud.com/ and the PLT Support Center at
https://plt.bcdevices.com/hc/en-us .
Page paths in this skill and its references are relative to https://docs.pltcloud.com/ — a page's URL is that base plus its path.
