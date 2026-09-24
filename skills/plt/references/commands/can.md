# CAN bus

## canCfg

Configure CAN interface

Configure a CAN interface. This command can be used to adjust the speed bit settings of a CAN port. Additionally, it can be used to configure additional CAN ports via USB.

```yaml
- command: canCfg <port> <bitrate> [fd]
  [retry: <retryCount>]
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [interface: <usbDeviceInterface>]
  [with:
    [- tq <tq>]
    [- phaseSeg1 <phaseSeg1>]
    [- phaseSeg2 <phaseSeg2>]
    [- propSeg <progSeg>]
    [- samplePoint <samplePoint>]
    [- sjw <sjw>]
    [- dataBitrate <dataBitrate>]
    [- dataTQ <dataTQ>]
    [- dataPropSeg <dataProgSeg>]
    [- dataPhaseSeg1 <dataPhaseSeg1>]
    [- dataPhaseSeg2 <dataPhaseSeg2>]
    [- dataSamplePoint <dataSamplePoint>]
    [- dataSJW <dataSJW>]]
```

| Argument | Description |
|---|---|
| `<port>` | CAN port name: CAN0, CAN1, CAN2, etc. CAN0 is the PLT's built-in port; CAN1 and above refer to externally attached USB CAN dongles. |
| `<bitrate>` | Nominal (arbitration-phase) CAN bit rate, in bits per second. Maximum 1000000 (1 Mbit/s) on the built-in CAN0 port. |
| `fd` | Enable CAN-FD on the port. Only supported on externally attached USB CAN-FD dongles — the built-in CAN0 port does not support CAN-FD and rejects this flag. |
| `<retryCount>` | Optional: Number of times to retry the test step |
| `<usbDeviceID>` | Optional: USB device identifiers: VID:PID. |
| `<usbDevicePath>` | Optional: USB device path: port. … .port. |
| `<usbDeviceInterface>` | Optional: USB device interface: interface_number. |
| `<with>` | Additional command parameters, used to fine-tune CAN bit timing beyond the nominal bitrate (and, for CAN-FD, the with: dataBitrate data-phase rate). All fields are optional and apply only to externally attached USB CAN dongles. (optional) tq - Time quantum count phaseSeg1 - PHASE-SEG1 value (1…8) phaseSeg2 - PHASE-SEG2 value (1…8) propSeg - PROP_SEG value (1…8) samplePoint - Sample point, as a fraction of bit time (0.000…0.999) sjw - Synchronization Jump Width (1…4) dataBitrate - CAN-FD data-phase bit rate, in bits per second (1…1000000) dataTQ - Data-phase time quantum count dataPropSeg - Data-phase PROP_SEG value (1…8) dataPhaseSeg1 - Data-phase PHASE-SEG1 value (1…8) dataPhaseSeg2 - Data-phase PHASE-SEG2 value (1…8) dataSamplePoint - Data-phase sample point, as a fraction of bit time (0.000…0.999) dataSJW - Data-phase Synchronization Jump Width (1…4) |

External USB CAN dongles can be configured as CAN ports by using the usbDeviceID, usbDevicePath, or usbDeviceInterface fields. The first canCfg step for a given USB port attaches and configures the underlying interface; a later canCfg step for the same port reconfigures it in place.

> **NOTE:** The built-in CAN0 port, which does not support CAN-FD and is limited to a 1 Mbit/s maximum bit rate, can not be redefined. This means that the usbDeviceID, usbDevicePath, and/or usbDeviceInterface parameters can't be set on CAN0.

Examples: STM32F4 Discovery (`samples/board/stm32f4_disco/`)
See also: `canClear`, `canMatch`, `canSend`, CAN Interaction (`TestPlanReference/can/`), Peripherals (`peripheral/`), CAN Dongles (`peripheral/can/`)
## canClear

Clear CAN Buffer

Clear the buffer of received CAN frames.

The PLT retains the most recently received frame for each CAN Arbitration ID on the port, and canMatch tests against that retained frame. canClear discards all retained frames for port, so a subsequent canMatch on that port only matches against frames received after the clear. Use it before a canSend/canMatch pair to avoid an unrelated, previously received frame with the same ID satisfying the match. Clearing one port does not affect any other CAN port.

```yaml
- command: canClear <port>
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<port>` | CAN port name: CAN0, CAN1, CAN2, etc. |
| `<retryCount>` | Number of times to retry the test step (optional) |

Examples: STM32F4 Discovery (`samples/board/stm32f4_disco/`)
See also: `canCfg`, `canMatch`, `canSend`, CAN Interaction (`TestPlanReference/can/`)
## canMatch

Match received CAN message

Test if a particular CAN message has been received.

The PLT keeps only the single most recently received frame for each Arbitration ID on port. canMatch polls that retained frame — it does not search a history of previously received frames — so if several frames with the same msgId arrive, only the latest one is checked. Use canClear beforehand to ensure a stale frame with the same ID doesn't cause a false match.

If the b payload bytes are omitted, the command succeeds as soon as any frame with the matching msgId is received, regardless of payload. If b bytes are given, they are matched against the received frame's payload as an exact-value prefix: the received payload must be at least as long as the number of b bytes supplied, and each supplied byte must equal the received byte at the same position. Trailing received bytes beyond the supplied b bytes are ignored — there is no partial-byte/wildcard mask. To check specific bytes without constraining the ones before them, supply all preceding bytes as well.

The command polls port until a matching frame arrives or the step times out. If no timeout: is set on the step, it defaults to 3 seconds.

```yaml
- command: canMatch <port> <msgId> [<b> <b> ...]
  [extractKey: <key>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<port>` | CAN port name: CAN0, CAN1, CAN2, etc. |
| `<msgId>` | CAN Message Arbitration ID (11-bit standard or 29-bit extended). Can be specified as a decimal, hex, or binary number, depending on prefix. Use 0x for hex and 0b for binary. If no prefix is specified, the value will be interpreted as decimal. |
| `<b>` | Payload bytes to match against a prefix of the received frame's data, in order, starting at byte 0. Each byte can be specified as a decimal, hex, or binary number, depending on prefix. Use 0x for hex and 0b for binary. If no prefix is specified, the value will be interpreted as decimal. Omit all b bytes to match on msgId alone, irrespective of payload. |
| `<key>` | Key in which to store the matching CAN message's payload, as a hex string (optional) |
| `<retryCount>` | Number of times to retry the test step (optional) |

> **NOTE:** The built-in CAN0 port does not support CAN-FD, so received frames on CAN0 are limited to 8-byte Classic CAN payloads. Frames longer than 8 bytes require an externally- attached USB CAN-FD dongle configured with FD via canCfg.

Examples: STM32F4 Discovery (`samples/board/stm32f4_disco/`)
See also: `canCfg`, `canClear`, `canSend`, CAN Interaction (`TestPlanReference/can/`)
## canSend

Send CAN message

Send a CAN data frame. If no payload bytes are given, a zero-length data frame is sent for the msgId.

```yaml
- command: canSend <port> <msgId> [<b> <b> ...] [nofd]
  [extractKey: <key>]
  [retry: <retryCount>]
  [with:
    [- flags <flags>]
    [- dlc <dlc>]]
```

| Argument | Description |
|---|---|
| `<port>` | CAN port name: CAN0, CAN1, CAN2, etc. |
| `<msgId>` | CAN Message Arbitration ID (11-bit standard or 29-bit extended). Can be specified as a decimal, hex, or binary number, depending on prefix. Use 0x for hex and 0b for binary. If no prefix is specified, the value will be interpreted as decimal. |
| `<b>` | Payload bytes, in order, starting at byte 0. Up to 8 bytes on Classic CAN, or up to 64 bytes on a port configured for CAN-FD (see canCfg). Each byte can be specified as a decimal, hex, or binary number, depending on prefix. Use 0x for hex and 0b for binary. If no prefix is specified, the value will be interpreted as decimal. |
| `nofd` | Send a Classic CAN frame on a port configured for CAN-FD, instead of a CAN-FD frame. Has no effect on a port that isn't configured for CAN-FD. Must be the last token on the command line, after all payload bytes. |
| `<key>` | Key in which to store the transmitted payload, as a hex string (optional) |
| `<retryCount>` | Number of times to retry the test step (optional) |
| `<flags>` | Optional: raw CAN-FD flags byte (0…15) to send with the frame. |
| `<dlc>` | Optional: DLC value to send when no payload bytes (b) are given, for example to send an empty frame that still advertises a non-zero data length code. Ignored if any payload bytes are supplied — in that case the DLC is derived from the payload length. |

> **NOTE:** The built-in CAN0 port does not support CAN-FD. CAN-FD frames (64-byte payloads, with: flags, nofd) are only available on externally-attached USB CAN-FD dongles that have been configured with FD via canCfg.

Examples: STM32F4 Discovery (`samples/board/stm32f4_disco/`)
See also: `canCfg`, `canClear`, `canMatch`, CAN Interaction (`TestPlanReference/can/`)
