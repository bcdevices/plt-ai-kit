# External instruments

## scpi

SCPI Interaction

Interact with an instrument using SCPI over USBTMC. Requires a supported USBTMC SCPI instrument attached to the PLT's USB host.

handle is a free-form name (no ., /, :, or whitespace/newline characters) used to identify the connected instrument across connect, command, and query steps.

### `scpi connect`

Locates the instrument's USBTMC device and configures handle for use. If neither id: nor path: is given, the PLT selects the sole USBTMC device present; specify id: or path: to disambiguate when more than one instrument is attached.

```yaml
- command: scpi connect <handle>
  [retry: <retryCount>]
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [interface: <usbDeviceInterface>]
  [with:
    - readTermination "<readTermination>"
    - writeTermination "<writeTermination>"
  ]
```

| Argument | Description |
|---|---|
| `<handle>` | Used to refer to this instrument in further commands. |
| `<retryCount>` | Optional: Number of times to retry the test step |
| `<usbDeviceID>` | Optional: USB device identifiers: VID:PID. |
| `<usbDevicePath>` | Optional: USB device path: port. … .port. |
| `<usbDeviceInterface>` | Optional: USB device interface: interface_number. Selects a specific interface when the device exposes more than one. |
| `<with>` | Optional: One or more SCPI configuration fields. Supported keys: readTermination "<readTermination>" — specifies the character or sequence of characters that signals the end of an incoming SCPI message (for example: "\r\n"). If readTermination is not specified, the PLT will return the first USBTMC response message, trimming any carriage return (\r) or newline (\n) characters. writeTermination "<writeTermination>" — specifies the character or sequence of characters that signals the end of an outgoing SCPI message. If writeTermination is not specified, the PLT will send a newline, followed by a NUL character (equivalent to writeTermination "\n\x00"). |

### `scpi command`

Send one or more SCPI commands (no response expected) to a previously connected instrument. The step fails if the transfer times out or the instrument reports an error.

The inline command argument, if given, is sent first; any with: entries are sent afterward, in list order. A step must specify at least one message, from either form.

```yaml
- command: scpi command <handle> [<command>]
  [retry: <retryCount>]
  [timeout: <timeout>]
  [with:
    [- <command>]
    [- <command>]
    [..]]
```

| Argument | Description |
|---|---|
| `<handle>` | Handle of a previously connected SCPI instrument |
| `<command>` | SCPI command (for example: "*RST") |
| `<retryCount>` | Number of times to retry the test step (optional) |
| `<timeout>` | Timeout, with suffix or in milliseconds (default: 5000ms) |

### `scpi query`

Send one or more SCPI queries to a previously connected instrument and capture the instrument's response text as the step result.

As with scpi command, the inline command argument (if given) is sent first, followed by any with: entries in list order; at least one query must be specified.

```yaml
- command: scpi query <handle> [<command>]
  [extractKey: <key>...]
  [retry: <retryCount>]
  [timeout: <timeout>]
  [with:
    [- <command>]
    [- <command>]
    [..]]
```

| Argument | Description |
|---|---|
| `<handle>` | Handle of a previously connected SCPI instrument |
| `<command>` | SCPI command query (for example: "*IDN?") |
| `<key>` | Key in which to store extracted text. |
| `<retryCount>` | Number of times to retry the test step (optional) |
| `<timeout>` | Timeout, with suffix or in milliseconds (default: 5000ms) |

Examples: Tektronix Keithley PSU 2230 Series (`samples/inst/tek_keithley_psu2230/`), Tektronix Keithley DMM6500 (`samples/inst/tek_keithley_dmm6500/`)
