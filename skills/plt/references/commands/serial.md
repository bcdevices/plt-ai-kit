# UART and serial

## ftdiCfg

Configure external FTDI [Deprecated]

Hardware: PLT-200A

Historical usage (PLT-200A, pltOS <= 1.8.0 only):

```yaml
- command: ftdiCfg FTDI1 <target> [<UARTxx>][,<UARTxx>[,<UARTxx>[,<UARTxx>]]]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<target>` | FTDI interface; only FTDI1 can be configured. |
| `<UARTxx>` | UART port to use for each FTDI port: UART2, UART3, .. , or _ to skip. |
| `<retryCount>` | Number of times to retry the test step (optional) |

> **WARNING:** ftdiCfg is deprecated and no longer provided. It is available for PLT-200A running pltOS <= 1.8.0, configuring an externally connected FTDI FT4232H module. Please migrate to, use the uartCfg command instead; the on-board FTDI UART adapter is configured automatically and does not require a separate ftdiCfg step.

See also: `uartCfg`
## uart

Send and Extract UART response

Send text to a UART port and/or wait for a response, optionally extracting values from the response into test plan keys.

If sendText is given, it is transmitted first. If expectText and/or extractText are given, the command then waits (up to timeout) for the receive buffer to contain a match; extractText is a regular expression matched against the most recent line of received text (see note below), and its capture groups are stored in the corresponding key names given by extractKey. If neither expectText nor extractText is given, the command sends and returns immediately without waiting on a response. Unless noflush is set, the receive buffer is flushed before waiting and the transmit buffer is flushed after sending.

```yaml
- command: uart <uartPort> [noflush]
  [expect: [hex] <expectText>]
  [extract: <extractText>]
  [extractKey: <key>...]
  [send: [hex] <sendText>]
  [retry: <retryCount>]
  [timeout: <timeout>]
```

| Argument | Description |
|---|---|
| `<uartPort>` | UART port name: UART0, UART1, UART2, etc. Must match a port configured (built-in or via uartCfg). |
| `<expectText>` | Text to expect in the response, prior to extraction. If the hex keyword is used, expectText is interpreted as a hex string. |
| `<extractText>` | Regular expression to extract from the response (uses RE2 Syntax, except \C). Each capture group is stored in the corresponding extractKey. |
| `<key>` | Key(s) in which to store extracted text. To save multiple values, use multiple capture groups. |
| `<sendText>` | Text to send before waiting for a response. If the hex keyword is used, sendText is interpreted as a hex string. |
| `noflush` | Don't flush the receive buffer before waiting, or the transmit buffer after sending. |
| `<retryCount>` | Number of times to retry the test step (optional) |
| `<timeout>` | Timeout, in milliseconds, to wait for expectText/extractText to match (default: 1000ms) |

Use uart for a single-step send/expect/extract exchange. For a fire-and-forget expectation set earlier and awaited later (e.g. across an intervening operator step), use uartExpect together with uartAwait instead.

> **NOTE:** The extract regular expression is matched within a single line of received text. Lines before the most recent line ending are discarded as data arrives, so a pattern must not depend on a preceding line or begin with \r\n/\n. A trailing \r\n to anchor the end of the line is fine. To capture values from several lines, use one uart step per line.

Examples: nRF52 DK (`samples/board/nrf52dk/`), HiFive Unmatched (`samples/board/hifive_unmatched/`), Console (`samples/linux/console/`), Nordic nRF Command Line Tools (`samples/ppcsbc/nordic-nrfjprog/`), NXP Secure Provisioning SDK (`samples/ppcsbc/nxp-spsdk/`), shell (`samples/zephyr/shell/`)
See also: `value`, `uartAwait`, `uartCfg`, `uartExpect`, `uartReadTimeout`, UART Interaction (`TestPlanReference/uart/`)
## uartAwait

Await UART response

Wait for the expectation previously set on this port with uartExpect to be matched. The step fails if the expected text is not received before the timeout elapses.

```yaml
- command: uartAwait <uartPort> [<seconds>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<uartPort>` | UART port name: UART0, UART1, UART2, etc. |
| `<seconds>` | Time to await the response, in seconds. A timeout must be set, either here or via a prior step's timeout:; if none is set, the step fails immediately. |
| `<retryCount>` | Number of times to retry the test step (optional) |

Pair uartAwait with uartExpect: set the expectation with uartExpect first, perform other steps (for example, prompting the operator or triggering the DUT), then call uartAwait to block until that expectation is matched or the timeout elapses. For a single-step send/expect exchange without an intervening step, use uart instead.

See also: `uart`, `uartCfg`, `uartExpect`, `uartReadTimeout`, UART Interaction (`TestPlanReference/uart/`)
## uartBreak

Control UART Break

Controls the UART break condition (forcing TX line low).

```yaml
- command: uartBreak <uartPort> on|off|<durationMs>
```

| Argument | Description |
|---|---|
| `<uartPort>` | UART port name: UART0, UART1, UART2, etc. |
| `on` | Assert break indefinitely (until a subsequent uartBreak <uartPort> off). |
| `off` | Clear a previously asserted break. |
| `<durationMs>` | Assert break for the given duration, in milliseconds, then clear it automatically. Must be at least 1. |

See also: `uart`, `uartAwait`, `uartCfg`, `uartExpect`, UART Interaction (`TestPlanReference/uart/`)
## uartCfg

Configure UART

Configure a UART port. This command can be used to adjust the baud rate and bit settings of a UART port. Additionally, it can be used to configure additional UART ports via USB.

```yaml
- command: uartCfg <uartPort> <speed> [<triplet>]
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [interface: <usbDeviceInterface>]
```

| Argument | Description |
|---|---|
| `<uartPort>` | UART port name: UART0, UART1, UART2, etc. |
| `<speed>` | Baud rate, in bits per second. Must be greater than 0 and no more than 3000000 (3 Mbps). |
| `<triplet>` | UART configuration triplet: 8N1 (8 data bits, no parity, 1 stop bit; default if omitted), 8E1 (8 data bits, even parity, 1 stop bit), or 7E1 (7 data bits, even parity, 1 stop bit). |
| `<usbDeviceID>` | Optional: USB device identifiers: VID:PID. |
| `<usbDevicePath>` | Optional: USB device path: port. ... .port. |
| `<usbDeviceInterface>` | Optional: USB device interface: interface_number. |

External USB serial interfaces can be configured as UART ports by using the usbDeviceID, usbDevicePath, or usbDeviceInterface fields. FTDI UART adapters and USB-CDC peripherals are supported.

**Probe multiplexing**

```yaml
- command: uartCfg UART0 tp
```

For UART0 on carrier boards with a probe multiplexer, uartCfg UART0 tp switches the UART0 multiplexer to use the debug test-point path instead of the standard UART0 connection. This form is not available for UART1 or higher-numbered ports. Configuring UART0's baud rate/triplet (the normal uartCfg UART0 <speed> ... form) switches the multiplexer back to the standard UART0 path.

> **NOTE:** The built-in UART ports cannot be redefined. That is, the usbDeviceID, usbDevicePath, and/or usbDeviceInterface parameters can't be set on UART0 or UART1.

> **NOTE:** Hardware flow control (RTS/CTS) and software flow control (XON/XOFF) are not currently supported; only no-flow-control configuration is available.

Examples: nRF52 DK (`samples/board/nrf52dk/`), HiFive Unmatched (`samples/board/hifive_unmatched/`), Nordic nRF Command Line Tools (`samples/ppcsbc/nordic-nrfjprog/`), NXP Secure Provisioning SDK (`samples/ppcsbc/nxp-spsdk/`)
See also: `ftdiCfg`, `uart`, `uartAwait`, `uartExpect`, `uartReadTimeout`, UART Interaction (`TestPlanReference/uart/`)
## uartExpect

Set expectation for uartAwait

Arm a UART response expectation to be waited on with a subsequent uartAwait command. This step itself does not block; it registers the expectation and returns immediately.

```yaml
- command: uartExpect <uartPort> <expect> [noflush]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<uartPort>` | UART port name: UART0, UART1, UART2, etc. |
| `<expect>` | String to expect with a subsequent uartAwait command. Prefix with hex to interpret as a hex string (e.g. hex ef0102). |
| `noflush` | Don't flush the receive buffer before registering the expectation. |
| `<retryCount>` | Number of times to retry the test step (optional) |

See also: `uart`, `uartAwait`, `uartCfg`, `uartReadTimeout`, UART Interaction (`TestPlanReference/uart/`)
## uartReadTimeout

Test if UART is not transmitting

Assert that nothing is received on a UART port. If sendText is given, it is sent first; the step then passes if no data arrives before the timeout elapses, and fails if any data is received.

```yaml
- command: uartReadTimeout <uartPort> [<seconds> [<sendText>]]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<uartPort>` | UART port name: UART0, UART1, UART2, etc. |
| `<seconds>` | Number of seconds to wait for incoming data. If omitted, the timeout in effect from a prior step's timeout: is used. |
| `<sendText>` | Text to send before waiting. Prefix with hex to interpret as hex bytes. |
| `<retryCount>` | Number of times to retry the test step (optional) |

The RX buffer is always flushed immediately before the silence-check begins, discarding any data received prior to the step (and prior to sending sendText, if given).

See also: `uart`, `uartAwait`, `uartCfg`, `uartExpect`, UART Interaction (`TestPlanReference/uart/`)
