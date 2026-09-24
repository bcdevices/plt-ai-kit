# Digital I/O and signal routing — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/digital-io.md`.

## mux

> **WARNING:** The Multiplexer sub-system of the PLT only tolerates voltages up to 5.5V.

## pin

> **NOTE:** On the PLT-300A, the DDTP00 ... DDTP08 pins need to be connected to the Multiplexer sub-system, to be used as GPIOs. Use the mux connect DDTPxx command to to connect such a pin to the Multiplexer sub-system.

> **WARNING:** When DDTPxx pins are connected to the Multiplexer sub-system, the maximum voltage is 5.5V.
