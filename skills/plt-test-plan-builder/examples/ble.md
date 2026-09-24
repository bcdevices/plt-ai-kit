# BLE Examples

Snippets for BLE discovery, GATT reads and writes, and low-level BLE testing.

## BLE Interaction

Source: `TestPlanReference/ble/`

**Discovery**

Example: BLE discovery of identified BLE HW MAC address.

```yaml
- ident: ICT-T1
  title: "Identify DUT"
  steps:
  - command: identify nRF52

- ident: ICT-T2
  title: "BLE Discovery"
  steps:
  - command: bledis %BLEMAC% 30 -60
```

**Commands**

- bledis (`TestPlanReference/command/bledis/`)

**GATT Interaction**

Example: Validate BLE Device Information Service

```yaml
title: "DIS Validation"
suite:

- ident: ICT-T1
  title: "Identify DUT"
  steps:
  - command: identify nRF52

- ident: ICT-T2
  title: "Program LY10-DEMO-BOARD FW"
  steps:
  - command: program nRF52 s132_nrf52_6.0.0_softdevice.hex,ly10-demo-fw-0.1.7.hex

- ident: ICT-T3
  title: "Validate BLE DIS"
  steps:
  - command: ble gatt connect addr:%ble_mac% 10
  - command: ble gatt discover
  # GAP:Device Name
  - command: ble gatt read char:2a00 4c5931302d44454d4f5f424f415244  # "LY10-DEMO_BOARD"
  # GAP Appearance
  - command: ble gatt read char:2a01 0000
  # GAP:Peripheral Preferred Connection Parameters
  - command: ble gatt read char:2a04 0600080200009001
  # GAP:Central Address Resolution
  - command: ble gatt read char:2aa6 01
  # DIS:Manufacturer Name String
  - command: ble gatt read char:2a29 424344 # "BCD"
  # DIS:Model Number String
  - command: ble gatt read char:2a24 4c5931302d44454d4f5f424f415244  # "LY10-DEMO_BOARD"
  # DIS:Hardware Revision String
  - command: ble gatt read char:2a27 32303139 # "2019"
  # DIS:Firmware Revision String
  - command: ble gatt read char:2a26 302e312e37 # "0.1.7"
  # DIS:Software Revision String
  - command: ble gatt read char:2a28 312e322e33 # "1.2.3"
  - command: ble gatt disconnect
```

**Commands**

- ble gatt (`TestPlanReference/command/ble_gatt/`)

**Low-Level BLE Testing**

Example: Receive BLE packets from DUT

```yaml
# Ensure dongle is not in DTM
- command: ble test stop

# Start receive by PLT on Channel 14
- command: ble test recv 14

# Send command to DUT to start transmit on Channel 14
- command: uart UART0
  send: "\r\nbt test_tx 0x0e 0x10 0 0x01\r\n"
  expect: "test_tx..."
- command: sleepms 3000 "Waiting 3s for transmits from DUT"

# Stop transmit by DUT
- command: uart UART0
  send: "\r\nbt test_end\r\n"
  expect: "num_rx= 0"

# Stop receive by PLT
- command: ble test stop
  extractKey: BLE_RX_COUNT

# Evaluate number of packets received from DUT
- command: eval "%BLE_RX_COUNT% > 3000"
```

Example: Send BLE packets to DUT

```yaml
# Ensure dongle is not in DTM
- command: ble test stop

# Send command to DUT to start receive on Channel 14
- command: uart UART0
  send: "\r\nbt test_rx 0x0e 0x01 0x00\r\n"
  expect: "test_rx..."

# Start transmit by PLT
- command: ble test xmit 14
- command: sleepms 3000 "Waiting 3s for DUT to receive"

# Stop transmit by PLT
- command: ble test stop

# Stop receive by DUT
- command: uart UART0
  send: "\r\nbt test_end\r\n"
  expect: "num_rx="
  extract: "num_rx= (.*).\r\n"
  extractKey: BLE_TX_COUNT

# Evaluate number of packets received by DUT
- command: eval "%BLE_TX_COUNT% > 3000"
```

**Commands**

- ble test (`TestPlanReference/command/ble_test/`)

> **NOTE:** Using the ble commands on PLT-300A requires a supported BLE test dongle (`peripheral/ble/`).
