# Programming and identification

## erase

Erase DUT Flash

Erase DUT MCU on-board flash.

```yaml
- command: erase <target> [<uartPort>]
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [interface: <usbDeviceInterface>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<target>` | Target to erase. A clock frequency may be appended as <target>@<freq> (for example STM32L4@200kHz) to override the default SWD/JTAG adapter speed; not all targets support this option. |
| `<uartPort>` | UART port name. Only required for UART programming targets. |
| `<usbDeviceID>` | Optional: Programming adapter USB device identifiers: VID:PID. |
| `<usbDevicePath>` | Optional: Programming adapter USB device path: port. ... .port. |
| `<usbDeviceInterface>` | Optional: Programming adapter USB device interface: interface_number. |
| `<retryCount>` | Optional: Number of times to retry the test step. |

```yaml
- command: erase CMSIS
  pack: <cmsisPack>
  target: <cmsisTarget>
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<target>` | Target to erase |
| `<cmsisPack>` | Optional: CMSIS Pack file. |
| `<cmsisTarget>` | Target name, as defined in CMSIS Pack file. |
| `<usbDeviceID>` | Optional: USB device identifiers: VID:PID. |
| `<usbDevicePath>` | Optional: USB device path: port. ... .port. |
| `<retryCount>` | Number of times to retry the test step (optional) |

On the PLT-300A, the programming adapter can be specified using usbDeviceID, usbDevicePath, and usbDeviceInterface. Specifying the programming adapter location allows multiple adapters of the same type to be used in a single test plan, or for an external adapter to be used in place of the built-in programming adapter. See USB Interaction (`TestPlanReference/usb/`) for details on specifying USB devices.

Supported `target` values: see `references/targets.md`, which lists every programming target with the commands that accept it.

> **NOTE:** USB-DFU targets cannot be erased with this command; the erase step will fail. USB-DFU devices are erased as part of program (unless noerase is specified).

> **NOTE:** The target list above covers commonly used programming targets. Additional MCU-specific targets (further STM32 and LPC family variants, TI CC13xx/CC26xx RFSoCs, additional PIC18 and AVR parts, and others) are supported by the underlying programmer; contact Blue Clover Devices if the target you need is not listed here.

Examples: Program Target Interaction (`TestPlanReference/prog/`)
## identify

Identify DUT

Identify DUT MCU and/or RF peripherals.

The MCU identifier is stored in the mcu_id key, and the BLE MAC address (if available) is stored in the ble_mac key.

```yaml
- command: identify <target> [<uartPort>]
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [interface: <usbDeviceInterface>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<target>` | Target to identify. A clock frequency may be appended as <target>@<freq> (for example STM32L4@200kHz) to override the default SWD/JTAG adapter speed; not all targets support this option. |
| `<uartPort>` | UART port name. Only required for UART programming targets. |
| `<usbDeviceID>` | Optional: Programming adapter USB device identifiers: VID:PID. |
| `<usbDevicePath>` | Optional: Programming adapter USB device path: port. ... .port. |
| `<usbDeviceInterface>` | Optional: Programming adapter USB device interface: interface_number. |
| `<retryCount>` | Optional: Number of times to retry the test step. |

On the PLT-300A, the programming adapter can be specified using usbDeviceID, usbDevicePath, and usbDeviceInterface. Specifying the programming adapter location allows multiple adapters of the same type to be used in a single test plan, or for an external adapter to be used in place of the built-in programming adapter. See USB Interaction (`TestPlanReference/usb/`) for details on specifying USB devices.

Supported `target` values: see `references/targets.md`, which lists every programming target with the commands that accept it.

> **NOTE:** identify is only implemented for the targets listed below (a specific subset of program/erase targets, since MCU identification requires vendor- and family-specific register reads). CMSIS, SDCard, and USB-DFU targets do not support identification. AVR targets are only supported when programmed via ISP or Xplained mini (_XPm); the FTDI and PICkit4 AVR variants, and all PIC18 targets, do not support identification.

## program

Program DUT

Erase and Program DUT MCU on-board flash.

### General usage

```yaml
- command: program <target> [<uartPort>] [offset:]<img>[,[offset:]<img>[,...]] [noerase]
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [interface: <usbDeviceInterface>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<target>` | Target to program. A clock frequency may be appended as <target>@<freq> (for example STM32L4@200kHz) to override the default SWD/JTAG adapter speed. Not all targets support this option; unsupported targets will fail this step. |
| `<uartPort>` | UART port name. Only required for UART programming targets. |
| `<offset>` | Optional: Image Address Offset, in decimal or 0x-prefixed hexadecimal. |
| `<img>` | Firmware File. A value of none skips that offset/image slot without error, leaving a gap in a multi-image program step. |
| `</home/runner/work/plt-docs/plt-docs/docs/TestPlanReference/command/program.rst:31: (INFO/1) Unexpected possible title overline or transition. Treating it as ordinary text because it's so short. ...>` | Optional: Additional offsets, images |
| `<noerase>` | Optional: If set, DUT will not be erased prior to programming. |
| `<usbDeviceID>` | Optional: Programming adapter USB device identifiers: VID:PID. |
| `<usbDevicePath>` | Optional: Programming adapter USB device path: port. ... .port. |
| `<usbDeviceInterface>` | Optional: Programming adapter USB device interface: interface_number. |
| `<retryCount>` | Optional: Number of times to retry the test step. |

On the PLT-300A, the programming adapter can be specified using usbDeviceID, usbDevicePath, and usbDeviceInterface. Specifying the programming adapter location allows multiple adapters of the same type to be used in a single test plan, or for an external adapter to be used in place of the built-in programming adapter. See USB Interaction (`TestPlanReference/usb/`) for details on specifying USB devices.

Firmware images can be provided as Intel HEX (.hex), ELF (.elf / .axf) or binary files (requiring an offset).

### Usage with CMSIS programming packs

```yaml
- command: program CMSIS [offset:]<img>
  pack: <cmsisPack>
  target: <cmsisTarget>
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<offset>` | Optional: Image Address Offset. |
| `<img>` | Firmware File. |
| `<cmsisPack>` | Optional: CMSIS Pack file. |
| `<cmsisTarget>` | Target name, as defined in CMSIS Pack file. |
| `<usbDeviceID>` | Optional: USB device identifiers: VID:PID. |
| `<usbDevicePath>` | Optional: USB device path: port. ... .port. |
| `<retryCount>` | Optional: Number of times to retry the test step. |

Firmware images can be provided as Intel HEX (.hex), ELF (.elf / .axf) or binary files (requiring an offset). Only one image may be specified for CMSIS programming.

### Usage with USB-DFU targets

```yaml
- command: program USB-DFU [offset:]<img>
  target: <target>
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<offset>` | Optional: Image Address Offset. |
| `<img>` | Firmware File. |
| `<target>` | Target MCU to program. |
| `<usbDeviceID>` | Optional: USB device identifiers: VID:PID. |
| `<usbDevicePath>` | Optional: USB device path: port. ... .port. |
| `<retryCount>` | Optional: Number of times to retry the test step. |

If neither usbDeviceID or usbDevicePath is set, the device connected to DUT USB-C Port (Port 1) is assumed. Only one image may be specified for USB-DFU programming.

For USB-DFU, firmware images must be in .dfu format. The dfuse-pack.py script from the dfu-util project <https://sourceforge.net/p/dfu-util/> can be used to generate .dfu files from hex or binary.

Supported `target` values: see `references/targets.md`, which lists every programming target with the commands that accept it.

> **NOTE:** The target list above covers commonly used programming targets. Additional MCU-specific targets (further STM32 and LPC family variants, TI CC13xx/CC26xx RFSoCs, additional PIC18 and AVR parts, and others) are supported by the underlying programmer; contact Blue Clover Devices if the target you need is not listed here.

Examples: Program Target Interaction (`TestPlanReference/prog/`)
