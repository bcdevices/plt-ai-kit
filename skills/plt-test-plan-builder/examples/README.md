# Bundled Examples

Two kinds of example: complete, working test plans from PLT sample
projects, and snippets for each DUT interface. Start from the closest plan,
then take the steps for each interface it needs from that interface's
snippet file.

## Snippets by interface

Step fragments from the Test Plan Reference guides. Most are not complete
plans; drop them into an item's `steps:`.

| Interface | File |
|---|---|
| Program a target: Test Agent and Flashr (`flashr-flash`), or the built-in identify / erase / program | `examples/programming.md` |
| UART send/expect/extract, expected timeouts | `examples/uart.md` |
| CAN configure, send and match frames | `examples/can.md` |
| BLE discovery, GATT, low-level testing | `examples/ble.md` |
| NFC detect and write | `examples/nfc.md` |
| USB device ID and paths, CDC, MSC, roles | `examples/usb.md` |

## Test plans

| Plan | Board | Commands used |
|---|---|---|
| `suite-nucleo_f401re-blinky.yaml` | nucleo_f401re | erase, identify, program |
| `suite-nucleo_h753zi-swd.yaml` | nucleo_h753zi | program |
| `suite-stm32f4_disco-sample-CAN.yaml` | stm32f4_disco | canCfg, canClear, canMatch, erase, identify, power, program, sleepms |

### What each plan demonstrates

- **Program only** (`nucleo_f401re`): the identify / erase / program sequence
  for the PLT's built-in programming interfaces. Stations with a Test Agent
  and Flashr program with `flashr-flash` instead; see
  `examples/programming.md`.
- **Programming plus a functional test** (`stm32f4_disco` CAN sample):
  configures a CAN interface, programs the DUT, then matches CAN frames the
  DUT sends, capturing one with `extractKey`.
- **Alternate programming interfaces** (`nucleo_h753zi`): the same board
  programmed over SWD, ST-Link, and USB-DFU. The USB-DFU plan carries the
  hardware setup its wiring depends on, as comments.

Full documentation for these boards is at https://docs.pltcloud.com/samples/board/ .
