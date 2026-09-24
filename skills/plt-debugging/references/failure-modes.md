# Failure Modes

Catalogued failures, with symptoms, diagnosis, and remedies. Hand-authored;
add entries under `curated/failure-modes/`.

## A measure step fails just outside its acceptance range

`measurement-out-of-range` · severity: common
 · PLT-300A
**Symptoms**
- A `measure` step fails on some units but not others.
- The reported value is close to the acceptance range, not wildly off.

**Diagnosis**
1. Confirm the measurement is referenced to the correct ground. On the PLT-300A a `measure` step can name a `ground:`; the wrong one shifts every reading.
1. Confirm the probe is routed correctly. Several PLT-300A probes must be connected through the multiplexer before they can be measured; if the `mux` routing is missing the reading is meaningless.
1. Check whether the acceptance range was set before real unit-to-unit spread was known. A range tighter than the true distribution fails good units.

**Remedies**
- Add or correct the `ground:` field on the `measure` step.
- Add the `mux connect` step the probe requires.
- Widen the acceptance range to the observed spread, only after confirming the units are actually good.

Related commands: `measure`, `mux`, `ground`
For full syntax see the `plt` skill's `references/commands/measurement.md`, the `plt` skill's `references/commands/digital-io.md`, the `plt` skill's `references/commands/power.md`. Aggregated gotchas for these commands are in `references/by-command/measurement.md`, `references/by-command/digital-io.md`, `references/by-command/power.md`.
## A program step fails to flash the DUT

`program-step-fails` · severity: common
 · PLT-300A, PLT-200A
**Symptoms**
- The `program` step fails, sometimes after `identify` succeeded, sometimes not.
- The failure is immediate rather than a timeout.

**Diagnosis**
1. Check that `identify` succeeds first. If it does not, the problem is the programming interface or target power, not the image.
1. Check that the DUT is powered. Programming needs the target rail on.
1. Check that the firmware image path resolves and the file was uploaded to the project.
1. On the PLT-300A, if several programming adapters of the same type are present, confirm the step targets the intended one by `id:`, `path:`, or `interface:`.

**Remedies**
- Fix target power or the programming interface before retrying.
- Correct the image path, or upload the missing image.
- Add `id:`/`path:`/`interface:` to disambiguate the adapter.

Related commands: `program`, `identify`, `erase`, `power`
For full syntax see the `plt` skill's `references/commands/programming.md`, the `plt` skill's `references/commands/power.md`. Aggregated gotchas for these commands are in `references/by-command/programming.md`, `references/by-command/power.md`.
