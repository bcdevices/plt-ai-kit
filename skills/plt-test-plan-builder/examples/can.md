# CAN Examples

Snippets for configuring a CAN interface and sending and matching frames.

## CAN Interaction

Source: `TestPlanReference/can/`

The PLT can be used to interact with CAN buses. The PLT can be used to send and receive CAN messages to verify CAN bus functionality.

**Configure CAN**

Example: Configure internal CAN interface

```yaml
- ident: CAN.CONFIG
  title: "Configure CAN0 to 250Kbit/sec"
  steps:
  - command: canCfg CAN0 250000
```

Example: Configure external CAN-FD interface

```yaml
- ident: CANFD.CONFIG
  title: "Configure CAN1 to 0.5/2 Mbit/sec"
  steps:
  - command: canCfg CAN1 500000 fd
    path: "5"
    with:
    - dataBitrate 2000000
```

> **NOTE:** CAN-FD is only supported using a USB-attached CAN test dongle (`peripheral/can/`).

**Commands**

- canCfg (`TestPlanReference/command/canCfg/`)

**Send and Receive**

Example: Send 4-byte CAN message with ID 0x123

```yaml
- title: "Send a CAN message"
  steps:
  - command: canSend CAN0 0x123 0x00 0x01 0x02 0x04
```

Example: Send an empty CAN (RTR) message with ID 0x123

```yaml
- title: "Send a CAN RTR message"
  steps:
  - command: canSend CAN0 0x123
```

Example: Receive 4-byte CAN message with ID 0x123

```yaml
- title: "Send and Receive CAN message"
  steps:
  # Clear CAN receive buffer to avoid matching against stale data.
  - command: canClear CAN0
  # Match CAN message with ID 0x123, within 1 second.
  # Save payload to user key for further interaction or reporting.
  - command: canMatch CAN0 0x123
    timeout: 1s
    extractKey: CAN_123_PAYLOAD
```

Example: Send CAN message, expect a response

```yaml
- ident: ICT-T1
  title: "Send a CAN message, expect response"
  steps:
  # Configure CAN0 to 250 kbit/s
  - command: canCfg CAN0 250000
  # Clear CAN receive buffer to avoid matching against stale data.
  - command: canClear CAN0
  # Send CAN message.
  - command: canSend CAN0 0x123 0x00 0x01 0x02 0x04
  # Match CAN message with ID 0x123 with specified payload, within 1 second.
  - command: canMatch CAN0 0x123 0x00 0x01 0x02 0x04
    timeout: 1s
```

- canClear (`TestPlanReference/command/canClear/`)
- canMatch (`TestPlanReference/command/canMatch/`)
- canSend (`TestPlanReference/command/canSend/`)
