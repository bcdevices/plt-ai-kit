# USB

## usb detect

USB Device Detection

Checks whether the specific USB device has been detected and enumerated by PLT.

PLT repeatedly scans the USB bus until a matching device is seen or timeout elapses, logging each device it observes (including devices that appear, disappear, or re-appear during the scan). This makes usb detect useful both for confirming a device is already present and for waiting on a device to enumerate after it is plugged in, powered on, or reset.

```yaml
- command: usb detect
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [retry: <retryCount>]
  [timeout: <duration>]
  [with:
    - <filterKey> <value>
    - <langid>:<index> "<stringValue>"
  ]
```

| Argument | Description |
|---|---|
| `<usbDeviceID>` | Optional: USB device identifiers: VID:PID, each in hex (for example 1366:0101 or 0x1366:0x0101). If set, only devices matching this VID:PID are considered. |
| `<usbDevicePath>` | Optional: USB device path: port. ... .port (see USB Device Paths). If set, only the device at this exact path is considered. |
| `<retryCount>` | Optional: Number of times to retry the test step. |
| `<timeout>` | Optional: Maximum duration to wait for detection (for example 5s). If omitted, PLT performs a single scan of the currently enumerated devices rather than waiting/polling for a device to appear. |
| `<with>` | Optional: One or more exact-match string filters. All specified filters must match. usbDeviceID and/or usbDevicePath may still be combined with with: to further narrow the candidate device(s). Supported keys: manufacturer <value> — exact match against the device's iManufacturer string. product <value> — exact match against the device's iProduct string. serial <value> — exact match against the device's iSerialNumber string. <langid>:<index> "<stringValue>" — exact match of the string descriptor at the given language ID (for example 0x0409 for US English) and descriptor index, useful for descriptors not exposed by the keys above. Values may optionally be wrapped in double or single quotes; matching is exact (case-sensitive), not a substring or glob match. |

Minimal device check:

```yaml
- command: usb detect
  id: "6666:8001"
  fail: "SBC not detected (USB)"
```

Match multiple strings:

```yaml
- command: usb detect
  id: "1366:0101"
  with:
    - manufacturer "SEGGER"
    - product "J-Link"
    - serial "000609300812"
```

Exact descriptor index:

```yaml
- command: usb detect
  id: "0525:a4a8"
  with:
    - 0x0409:1 "QR Scanner"
```

> **NOTE:** If neither usbDeviceID nor usbDevicePath is set, path: "1" (The DUT USB-C Port) is used.

See also: `usb power`, `usb reset`, `usb storage`, `uartCfg`, USB Interaction (`TestPlanReference/usb/`)
## usb power

USB Port Power Control

Control USB port power.

usb power switches power on both the USB 2.0 and USB 3.0 legs of the addressed port so that, on a dual-speed connection, the port is fully powered or fully unpowered rather than left in a mixed state.

```yaml
- command: usb power on|off
  [path: <usbDevicePath>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `on` | Enable port and turn on port power. |
| `off` | Disable port and turn off port power. |
| `<usbDevicePath>` | Optional: USB device path: port. ... .port (see USB Device Paths). Unlike usb detect and usb reset, usb power does not accept an id: <usbDeviceID> argument — power is applied to a hub port, not to a device identified by VID:PID, so the target must always be given as a path. |
| `<retryCount>` | Optional: Number of times to retry the test step. |

> **NOTE:** Turning off port power effectively disables the port. Even devices that don't require power through the port will not work when port power is off.

> **NOTE:** Port power can only be controlled if the port is on a hub (like the internal hubs in PLT-300A) that support power control. List of known compatible hubs.

> **NOTE:** If usbDevicePath is not set, path: "1" (The DUT USB-C Port) is used.

Examples: STM32 Nucleo H753ZI (`samples/board/nucleo_h753zi/`), nRF52 DK (`samples/board/nrf52dk/`)
See also: `uartCfg`, `usb detect`, `usb reset`, `usb storage`, USB Interaction (`TestPlanReference/usb/`)
## usb reset

USB Reset

Issues a USB port reset to a single USB device, without removing power from the port. PLT locates the device (by id, by path, or by the default DUT USB-C port) and asks the host controller to reset it, which causes the device to briefly disconnect and re-enumerate as it would after a cable reconnect. Use usb reset to recover a device that is stuck or unresponsive, or to force re-enumeration (for example, after reprogramming a device that needs to reload its USB descriptors) without cycling port power with usb power.

```yaml
- command: usb reset
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<usbDeviceID>` | Optional: USB device identifiers: VID:PID, each in hex (for example 1366:0101). Selects the device to reset. |
| `<usbDevicePath>` | Optional: USB device path: port. ... .port (see USB Device Paths). Selects the device to reset. |
| `<retryCount>` | Optional: Number of times to retry the test step. |

> **NOTE:** If neither usbDeviceID nor usbDevicePath is set, path: "1" (The DUT USB-C Port) is used.

See also: `uartCfg`, `usb detect`, `usb power`, `usb storage`, USB Interaction (`TestPlanReference/usb/`)
## usb storage

USB Storage

Interact with USB Mass Storage Devices

### `usb storage mount`

Mount a USB Mass Storage Device's filesystem.

PLT locates the device (by id, by path, or by the default DUT USB-C port), reads its USB serial number, finds the corresponding block device, and mounts its first partition read-write on the PLT host under an internal mount point associated with handle. Subsequent usb storage commands, such as write and unmount below, refer to the device by handle rather than by id/path.

```yaml
- command: usb storage mount <handle>
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<handle>` | Name used to refer to this mounted device in subsequent usb storage commands. Must not contain ., /, :, or whitespace/newline characters. |
| `<usbDeviceID>` | Optional: USB device identifiers: VID:PID, each in hex (for example 1366:0101). |
| `<usbDevicePath>` | Optional: USB device path: port. ... .port (see USB Device Paths). |
| `<retryCount>` | Optional: Number of times to retry the test step. |

### `usb storage unmount`

Unmount a previously mounted USB Mass Storage filesystem.

PLT attempts a normal (lazy) unmount first; if that fails, it retries with a forced unmount. Once unmounted, handle is no longer valid and must be mounted again (with usb storage mount) before further use.

```yaml
- command: usb storage unmount <handle>
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<handle>` | Handle of a previously mounted USB Mass Storage device. |
| `<retryCount>` | Optional: Number of times to retry the test step. |

### `usb storage write`

Write a file to a previously mounted USB Mass Storage Device.

fileName is read from the PLT host's local filesystem (not the DUT's) and copied onto the mounted device, overwriting any existing file at the destination. fileName must be a bare filename (no /) — this prevents using this command to copy arbitrary files off the PLT by path traversal.

```yaml
- command: usb storage write <handle> <fileName> [<filePath>] [decompress]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<handle>` | Handle of a previously mounted USB Mass Storage device. |
| `<fileName>` | Bare name (no path separators) of the file to write, resolved on the PLT host. |
| `<filePath>` | Optional: Destination path on the mounted device's filesystem. Default is /, i.e. the file is written to the root of the device using its original fileName. If filePath ends in /, the file is written into that directory under fileName; otherwise filePath is used as the full destination path (including filename) on the device. Must not contain ... |
| `<decompress>` | Optional literal flag: decompress. Not yet implemented; if present, the command currently fails. |
| `<retryCount>` | Optional: Number of times to retry the test step. |

> **NOTE:** If neither usbDeviceID nor usbDevicePath is set, path: "1" (The DUT USB-C Port) is used.

Examples: Raspberry Pi Pico (`samples/board/rpi_pico/`), Nordic nRF Command Line Tools (`samples/ppcsbc/nordic-nrfjprog/`), NXP Secure Provisioning SDK (`samples/ppcsbc/nxp-spsdk/`)
See also: `uartCfg`, `usb detect`, `usb power`, `usb reset`, USB Interaction (`TestPlanReference/usb/`), Program Targets (`target/`), Generic (`target/generic/`), SD-Card (`target/generic/sdcard/`), USB Mass Storage device (`target/generic/usb-msd/`)
