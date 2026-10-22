# UART and serial — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/serial.md`.

## ftdiCfg

> **WARNING:** ftdiCfg is deprecated and no longer provided. It is available for PLT-200A running pltOS <= 1.8.0, configuring an externally connected FTDI FT4232H module. Please migrate to, use the uartCfg command instead; the on-board FTDI UART adapter is configured automatically and does not require a separate ftdiCfg step.

## uart

> **NOTE:** The extract regular expression is matched within a single line of received text. Lines before the most recent line ending are discarded as data arrives, so a pattern must not depend on a preceding line or begin with \r\n/\n. A trailing \r\n to anchor the end of the line is fine. To capture values from several lines, use one uart step per line.

## uartCfg

> **NOTE:** The built-in UART ports cannot be redefined. That is, the usbDeviceID, usbDevicePath, and/or usbDeviceInterface parameters can't be set on UART0 or UART1.

> **NOTE:** Hardware flow control (RTS/CTS) and software flow control (XON/XOFF) are not currently supported; only no-flow-control configuration is available.
