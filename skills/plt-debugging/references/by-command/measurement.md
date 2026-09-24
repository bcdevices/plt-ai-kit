# Measurement — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/measurement.md`.

## measure

> **NOTE:** For the voltageDiff channel, 2 signal names must be provided, separated with a -. For example: DATP00-DATP01 for a differential measurement between DATP00 and DATP01.

> **NOTE:** For the continuity channel, acceptance is a boolean value (True/False, 1/0, t/f) indicating whether continuity is expected between signal and ground.

> **CAUTION:** In order to avoid damage to the PLT, take care that signals are below the Max Voltage for the selected measurement channel.

> **NOTE:** On the PLT-300A, the DATP00 ... DATP06 pins need to be connected to the Multiplexer sub-system, in order to use voltageDATP00 ... voltageDATP06. Use the mux connect DDTPxx command to to connect such a pin to the Multiplexer sub-system.
