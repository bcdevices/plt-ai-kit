# USB — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/usb.md`.

## usb detect

> **NOTE:** If neither usbDeviceID nor usbDevicePath is set, path: "1" (The DUT USB-C Port) is used.

## usb power

> **NOTE:** Turning off port power effectively disables the port. Even devices that don't require power through the port will not work when port power is off.

> **NOTE:** Port power can only be controlled if the port is on a hub (like the internal hubs in PLT-300A) that support power control. List of known compatible hubs.

> **NOTE:** If usbDevicePath is not set, path: "1" (The DUT USB-C Port) is used.

## usb reset

> **NOTE:** If neither usbDeviceID nor usbDevicePath is set, path: "1" (The DUT USB-C Port) is used.

## usb storage

> **NOTE:** If neither usbDeviceID nor usbDevicePath is set, path: "1" (The DUT USB-C Port) is used.
