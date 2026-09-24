# Programming and identification — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/programming.md`.

## erase

> **NOTE:** USB-DFU targets cannot be erased with this command; the erase step will fail. USB-DFU devices are erased as part of program (unless noerase is specified).

> **NOTE:** The target list above covers commonly used programming targets. Additional MCU-specific targets (further STM32 and LPC family variants, TI CC13xx/CC26xx RFSoCs, additional PIC18 and AVR parts, and others) are supported by the underlying programmer; contact Blue Clover Devices if the target you need is not listed here.

## identify

> **NOTE:** identify is only implemented for the targets listed below (a specific subset of program/erase targets, since MCU identification requires vendor- and family-specific register reads). CMSIS, SDCard, and USB-DFU targets do not support identification. AVR targets are only supported when programmed via ISP or Xplained mini (_XPm); the FTDI and PICkit4 AVR variants, and all PIC18 targets, do not support identification.

## program

> **NOTE:** The target list above covers commonly used programming targets. Additional MCU-specific targets (further STM32 and LPC family variants, TI CC13xx/CC26xx RFSoCs, additional PIC18 and AVR parts, and others) are supported by the underlying programmer; contact Blue Clover Devices if the target you need is not listed here.
