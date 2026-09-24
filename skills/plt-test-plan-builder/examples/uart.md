# UART Examples

Snippets for configuring a UART, sending and matching data, extracting keys, and testing for expected timeouts.

## UART Interaction

Source: `TestPlanReference/uart/`

**Configure UART**

Configure UART1 at 9600 baud, 8 data bits, no parity, 1 stop bit:

```yaml
- command: uartCfg UART1 9600 8N1
```

Configure channel 1 on an external FT4232-based FTDI FT4232H Mini Module (`peripheral/serial/ft4232h-mini-module/`) USB to UART adapter as UART2:

```yaml
- command: uartCfg UART2 115200
  path: "1"
  interface: "1"
  id: "0x0403:0x6011"
```

**Commands**

- uartCfg (`TestPlanReference/command/uartCfg/`)
- ftdiCfg (`TestPlanReference/command/ftdiCfg/`)

**Send and Receive**

Example: extract ICCID from cellular modem, storing in the ICCID key.

```yaml
- command: uart UART0
  expect: "+CCID:"
  extract: "CCID: (\\d{20})\r\n"
  extractKey: ICCID
  send: "AT+ICCID\r\n"
```

Example: extract multiple keys at once

```yaml
- command: uart UART0
  send: "\r\nkernel version\r\n"
  extract: "\r\n(.*) version (.*)\r\n"
  extractKey: KERNEL_NAME KERNEL_VERSION
```

Example: send and expect bytes from hex strings.

```yaml
- command: uart UART0
  send: hex "decafe01"
  expect: hex "badc0ffee1"
```

Example: expect string

```yaml
- command: uartExpect UART0 Pressed
- command: operator "Press button"
- command: uartAwait UART0 1
```

Example: expect bytes

```yaml
- command: uartExpect UART0 "hex ef0102"
- command: operator "Press button"
- command: uartAwait UART0 1
```

**Commands**

- uart (`TestPlanReference/command/uart/`)
- uartAwait (`TestPlanReference/command/uartAwait/`)
- uartExpect (`TestPlanReference/command/uartExpect/`)

**Expected Timeouts**

Example: test for read timeout after sending a string

```yaml
- command: uartReadTimeout UART0 1 "AT"
```

Example: test for read timeout after sending bytes

```yaml
- command: uartReadTimeout UART0 1 "hex badc0ffee1"
```

**Commands**

- uart (`TestPlanReference/command/uart/`)
- uartAwait (`TestPlanReference/command/uartAwait/`)
- uartExpect (`TestPlanReference/command/uartExpect/`)
- uartReadTimeout (`TestPlanReference/command/uartReadTimeout/`)
