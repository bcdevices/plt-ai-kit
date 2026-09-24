# CAN bus — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/can.md`.

## canCfg

> **NOTE:** The built-in CAN0 port, which does not support CAN-FD and is limited to a 1 Mbit/s maximum bit rate, can not be redefined. This means that the usbDeviceID, usbDevicePath, and/or usbDeviceInterface parameters can't be set on CAN0.

## canMatch

> **NOTE:** The built-in CAN0 port does not support CAN-FD, so received frames on CAN0 are limited to 8-byte Classic CAN payloads. Frames longer than 8 bytes require an externally- attached USB CAN-FD dongle configured with FD via canCfg.

## canSend

> **NOTE:** The built-in CAN0 port does not support CAN-FD. CAN-FD frames (64-byte payloads, with: flags, nofd) are only available on externally-attached USB CAN-FD dongles that have been configured with FD via canCfg.
