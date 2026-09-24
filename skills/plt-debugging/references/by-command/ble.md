# BLE — Documented Gotchas

Full command syntax, arguments and hardware limits are in the `plt` skill's
`references/commands/ble.md`.

## ble gatt

> **NOTE:** Using the ble gatt command on a PLT-300A requires a supported BLE test dongle.

> **NOTE:** Use ble gatt to exercise the DUT's application-level BLE stack (GATT services and characteristics). This is a way to perform a functional test of a product's BLE features. Use ble test for RF-only, link-layer transmitter/receiver tests (no GATT involved), and bledis for a simple presence/discovery check without reading or writing any characteristic.

## ble test

> **NOTE:** Using the ble test commands on a PLT-300A requires a supported BLE test dongle.

> **NOTE:** ble test drives the BLE radio directly (HCI-level LE transmitter/receiver test) to validate RF performance — it does not connect to the DUT's GATT server. Use ble gatt for functional tests of the DUT's BLE application, and bledis to confirm the DUT is advertising and discoverable.

## bledis

> **NOTE:** Using the bledis command on a PLT-300A requires a supported BLE test dongle.

> **NOTE:** bledis connects to the DUT and discovers its GATT services, then disconnects — it is a quick presence/discoverability check. Use ble gatt when the test plan needs to read, write, or match against specific characteristic values after connecting.
