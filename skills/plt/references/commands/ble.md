# BLE

## ble gatt

GATT-level BLE Tests

Perform GATT-level BLE interactions with the DUT.

```yaml
- command: ble gatt connect addr:<address> [<timeout> [<minRSSI>]]
  [retry: <retryCount>]

- command: ble gatt connect name:<name> [<timeout> [<minRSSI>]]
  [retry: <retryCount>]

- command: ble gatt disconnect
  [retry: <retryCount>]

- command: ble gatt discover
  [retry: <retryCount>]

- command: ble gatt match char:<charUUID> <matchHex>
  [retry: <retryCount>]

- command: ble gatt read char:<charUUID> <matchHex>
  [retry: <retryCount>]

- command: ble gatt sub char:<charUUID>
  [retry: <retryCount>]

- command: ble gatt write char:<charUUID> <valueHex>
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<name>` | GAP name advertised by the DUT, given as name:<name>. |
| `<address>` | DUT's BLE MAC address (XX:XX:XX:XX:XX:XX), given as addr:<address>. |
| `<timeout>` | Connect timeout, in seconds (default: 5s). |
| `<minRSSI>` | Minimum RSSI, in dBm, required to accept an advertisement during connect (optional; default: no filtering). |
| `connect` | Connect to the GATT peripheral, by address or by advertised name. |
| `disconnect` | Disconnect from the GATT peripheral. Succeeds (result not connected) even if no connection is active. |
| `discover` | Discover GATT services and characteristics on the connected peripheral. Fails if no services are found. |
| `match` | Poll a characteristic, waiting up to matchTimeout for its value to equal matchHex. Does not require a prior sub. |
| `read` | Read a GATT characteristic's current value. |
| `sub` | Subscribe to notifications from a GATT characteristic. |
| `write` | Write to a GATT characteristic. |
| `<charUUID>` | Characteristic UUID (16-bit short form or full 128-bit UUID), given as char:<charUUID>. |
| `<matchHex>` | For match: hex-encoded bytes the characteristic's value must equal. For read: an optional hex-encoded prefix; the step fails if the characteristic's value (as hex) does not start with this prefix. |
| `<matchTimeout>` | Timeout, in seconds, for match to wait for the expected value (optional; default: 5s). |
| `<valueHex>` | Hex-encoded bytes to write to the characteristic. |
| `<retryCount>` | Number of times to retry the test step (optional) |

match accepts an optional timeout as a third argument (ble gatt match char:<charUUID> <matchHex> [<matchTimeout>]); connect accepts optional timeout and minRSSI as shown above.

> **NOTE:** Using the ble gatt command on a PLT-300A requires a supported BLE test dongle.

> **NOTE:** Use ble gatt to exercise the DUT's application-level BLE stack (GATT services and characteristics). This is a way to perform a functional test of a product's BLE features. Use ble test for RF-only, link-layer transmitter/receiver tests (no GATT involved), and bledis for a simple presence/discovery check without reading or writing any characteristic.

Examples: BLE Interaction (`TestPlanReference/ble/`), BLE test dongle (`peripheral/ble/`)
## ble test

Low-level BLE Tests

Perform Low-level BLE tests.

```yaml
- command: ble test recv <channel>
  [retry: <retryCount>]

- command: ble test xmit <channel> [<length> [<payload>]]
  [retry: <retryCount>]

- command: ble test stop
  [extractKey: <key>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<channel>` | BLE link-layer test channel (0…39). Maps to RF channel frequency as 2402 MHz + 2*channel (channel 0 = 2402 MHz, channel 39 = 2480 MHz). |
| `<length>` | Length in bytes of payload data in each packet (0…255; default: 0 if omitted). |
| `<payload>` | Test packet payload type (0…255; default: 0 if omitted). Defined values: 0: PRBS9, 1: 0xF0, 2: 0xAA, 3: PRBS15, 4: 0xFF, 5: 0x00, 6: 0x0F, 7: 0x55. |
| `<key>` | Key in which to store the ble test stop result: the number of packets received since the test started (only meaningful after ble test recv was running). |
| `<retryCount>` | Number of times to retry the test step (optional) |

ble test xmit and ble test recv start a continuous LE transmitter or receiver test on the adapter's radio; they do not by themselves stop or time out. Use ble test stop to end the active test — for recv, this also returns the number of packets received.

> **NOTE:** Using the ble test commands on a PLT-300A requires a supported BLE test dongle.

> **NOTE:** ble test drives the BLE radio directly (HCI-level LE transmitter/receiver test) to validate RF performance — it does not connect to the DUT's GATT server. Use ble gatt for functional tests of the DUT's BLE application, and bledis to confirm the DUT is advertising and discoverable.

Examples: BLE Interaction (`TestPlanReference/ble/`), BLE test dongle (`peripheral/ble/`)
## bledis

Test BLE Discovery

Establishes a BLE connection to the DUT and discovers GATT services.

```yaml
- command: bledis %BLEMAC%|<name> [<timeout> [<minRSSI>]]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<name>` | GAP name advertised by the DUT, or its BLE MAC address (XX:XX:XX:XX:XX:XX). %BLEMAC% substitutes a previously-captured MAC address user key. |
| `<timeout>` | Discovery/connect timeout, in seconds (default: 5s). |
| `<minRSSI>` | Minimum RSSI, in dBm, required to accept an advertisement (optional; default: no filtering). |
| `<retryCount>` | Number of times to retry the test step (optional) |

The first argument is treated as a MAC address only if it is exactly 17 characters long and matches the XX:XX:XX:XX:XX:XX pattern (hex octets separated by colons); otherwise it is treated as a GAP device name. This makes %BLEMAC% and a literal MAC address interchangeable with a plain device name in the same argument position.

> **NOTE:** Using the bledis command on a PLT-300A requires a supported BLE test dongle.

> **NOTE:** bledis connects to the DUT and discovers its GATT services, then disconnects — it is a quick presence/discoverability check. Use ble gatt when the test plan needs to read, write, or match against specific characteristic values after connecting.

Examples: BLE Interaction (`TestPlanReference/ble/`), BLE test dongle (`peripheral/ble/`)
