# Test Agent

## agentCfg

Configure Agent

To facilitate SBC interaction during production, include an x86-64 PC or an additional SBC in the test fixture.

Interaction is configured based on how the agent is attached. The command auto-detects the connection type from the attached USB device (or from the identifier format given in id:) and configures it accordingly:

- USB-CDC: Configures the UART (USB-CDC, 1,000,000 baud 8N1) for an SBC running an agentOS image (for example, a PLT Test Agent), then starts a console session and optionally transfers files to its RAMDISK over USB Mass Storage.
- USB-NET or Ethernet: Derives an IPv6 link-local address from the agent's MAC address (or uses an IPv4/IPv6 address given directly) and configures a PLT agent session over the link-local network, optionally transferring files.

If <handle> has not been configured yet, the first call to agentCfg creates it, resolving the USB device or network address described by id:/path:/interface:. A later agentCfg on the same handle reuses the existing agent; the UART port cannot be changed on an already-configured handle.

```yaml
- command: agentCfg <handle> [<uartPort>]
  [retry: <retryCount>]
  [id: <agentID>]
  [path: <usbDevicePath>]
  [interface: <usbDeviceInterface>]
  [extractKey: <key>]
  [with:
    [- <fileName>]
    ...]
```

| Argument | Description |
|---|---|
| `<handle>` | Used to refer to this agent in further commands. |
| `<uartPort>` | Optional: UART port to use, for example UART2. Defaults to the port already assigned to handle, or to the port auto-detected for a USB-CDC agent. |
| `<retryCount>` | Optional: Number of times to retry the test step |
| `<fileName>` | Optional: Name of file to write to the SBC. |
| `<key>` | Optional: Key in which to store the UART port |
| `<agentID>` | Optional: Identifies the agent. Accepts a prefixed form or a bare legacy form (see below). Defaults to 6666:8001 (USB VID:PID) when omitted. |
| `<usbDevicePath>` | Optional: USB device path: port. … .port. |
| `<usbDeviceInterface>` | Optional: USB device interface: interface_number. |

**Agent ID formats**

If id: cannot be parsed by any of the above, agentCfg falls back to treating it as a legacy raw USB device identifier.

**PLT-200A / legacy id: forms**

```yaml
- command: agentCfg <handle> [<uartPort>]
  [retry: <retryCount>]
  [id: <usbDeviceID | macAddress>]
  [path: <usbDevicePath>]
  [extractKey: <key>]
  [with:
    [- <fileName>]
    ...]
```

| Argument | Description |
|---|---|
| `<usbDeviceID>` | Optional: USB device identifiers: VID:PID. |
| `<macAddress>` | Optional: Ethernet MAC address: XX:XX:XX:XX:XX:XX. |

**References**

- bcdevices/pypltagent-eth: Python pltagent, allowing a PLT to control an SBC/PC over Ethernet (https://github.com/bcdevices/pypltagent-eth)

_id: accepts either an explicit, prefixed form or a bare legacy form that is inferred heuristically. Prefixed forms are preferred, since the legacy heuristics can be ambiguous:_

| Form | Example / meaning |
|---|---|
| ip4:<address> | ip4:192.168.1.100 |
| ip6:<address> | ip6:fe80::1 |
| mac:<address> | mac:AA:BB:CC:DD:EE:FF — resolved to an IPv6 link-local address for USB-NET/Ethernet agents |
| vid:<VVVV>:<PPPP> | vid:6666:8001 — USB device selected by VID:PID |
| vid:<VVVV>:<PPPP>:mac:<address> | USB-Ethernet adapter selected by VID:PID, with its MAC validated against <address> |
| usb:<path> | usb:1.2.3 — equivalent to using path: |
| usb:<path>:mac:<address> | USB-Ethernet adapter selected by path, with its MAC validated against <address> |
| (bare) VVVV:PPPP | 6666:8001 — heuristically detected as VID:PID |
| (bare) XX:XX:XX:XX:XX:XX | heuristically detected as a MAC address |
| (bare) dotted decimal | heuristically detected as an IPv4 address |
| (bare) containing :: or 7+ colons | heuristically detected as an IPv6 address |

> **NOTE:** These bare id: forms are the older way of identifying an agent, used on a PLT-200A and by test plans written before the prefixed Agent ID formats above were added. They are still parsed heuristically (see the (bare) rows in that table) and continue to work on a PLT-200A, but new test plans should prefer the prefixed vid:/mac: forms, since the bare heuristics can be ambiguous.

> **NOTE:** For Ethernet-based control, the PLT agent package should be installed on the Agent PC. pypltagent-0.1.4.noarch.deb

Examples: Segger J-Link Software (`samples/ppcsbc/segger-commander/`), Nordic nRF Util (`samples/ppcsbc/nordic-nrfutil/`), RPi Camera Module (`samples/ppcsbc/rpi-camera/`)
See also: `agentExec`, Blue Clover Test Agent PER-101 (`peripheral/ta/per-101/`)
## agentExec

Execute command on Agent

Execute a command on an SBC or PC running a PLT Agent and await its completion. The agent handle must already be configured with agentCfg; agentExec fails if the handle is unknown.

Execution differs by connection type:

- Ethernet/USB-NET agents (link-local) send the command line to the agent and await a completed response; a non-zero/FAIL result fails the step and returns the agent's log output.
- USB-CDC agents send the command line over the UART console, appending a shell snippet that echoes a unique tag and the command's exit status. The step fails if that tag is not seen before the timeout, or if the command's exit status is non-zero.

```yaml
- command: agentExec <handle> <commandLine>
  [retry: <retryCount>]
  [timeout: <timeout>]
```

| Argument | Description |
|---|---|
| `<handle>` | Indicates the agent to use, as configured with agentCfg. |
| `<commandLine>` | Command line to execute through the agent. |
| `<retryCount>` | Optional: Number of times to retry the test step |
| `<timeout>` | Optional: Timeout waiting for the command to complete, with suffix or in milliseconds (default: 1000ms). Applies to USB-CDC (UART) agents. |

Examples: RPi Camera Module (`samples/ppcsbc/rpi-camera/`), Nordic nRF Util (`samples/ppcsbc/nordic-nrfutil/`)
See also: `agentCfg`, Blue Clover Test Agent PER-101 (`peripheral/ta/per-101/`)
