# Power and ground

## ground

Ground Selection

Hardware: PLT-300A

Select which DUT ground signals (GND1, GND2, GND3 and/or GND4) should be connected to the PLT system ground.

This affects power supply to the DUT, DDTPxx logic, DUT interaction over UART or USB, and measurements taken against PLT system ground.

```yaml
- command: ground none|<range>|all
```

| Argument | Description |
|---|---|
| `none` | Disconnect all GNDx signals from PLT system ground. |
| `<range>` | DUT ground indices or ranges to connect to PLT system ground; see the range examples below. |
| `all` | Connect all GNDx signals to PLT system ground. |

A range is a comma-separated list of ground indices (1-4) and/or inclusive index ranges (<low>-<high>). Any GNDx signal not named in range is left disconnected from PLT system ground. Example range values:

- 1: GND1
- 1-2,4: GND1 through GND2, and GND4
- 2,4: GND2 and GND4

> **NOTE:** Ground selection is only supported on PLT-300A, not on PLT-200A.

Examples: Fixture Control (`TestPlanReference/fixture/`)
## power

Power Control

Control power applied to the Device Under Test.

power off (with no rail) turns off all DUT power rails. power <rail> off turns off only the specified rail.

```yaml
- command: power off

- command: power <rail> [on|off|<level>]
```

| Argument | Description |
|---|---|
| `<rail>` | Power rail |
| `on` | Turn on the specified power rail |
| `off` | Turn off all or specified power rail |
| `<level>` | Voltage level for VARV, SWD or JTAG. Accepts a bare number (interpreted as volts) or a number with a V unit suffix (mV, V, kV); e.g., 3.3 and 3300mV are equivalent. |

Supported level values for the VARV rail: any value from 0.1 … 23.9 configures the adjustable supply to that voltage. 12.0 and 24.0 (within a small tolerance) instead switch VARV onto the fixed 12V and 24V rails rather than the adjustable supply. Requesting 0 while VARV is already on re-enables it at its previously configured voltage.

Supported level values for the SWD rail: 1.8, 3.3

Supported level values for the JTAG rail: 1.8, 3.3

_Supported rail values:_

| rail | Description |
|---|---|
| 1V8 | 1.8V power rail |
| 3V3 | 3.3V power rail |
| 5V | 5V power rail |
| VARV | Variable power rail |
| 12V | 12V power rail |
| 24V | 24V power rail |
| SWD | SWD target-voltage rail (1.8V or 3.3V, selectable) |
| JTAG | JTAG target-voltage rail (1.8V or 3.3V, selectable) |
| UART0 | UART0 (3.3V) power rail |
| UART1 | UART1 (3.3V) power rail |

> **NOTE:** level is only meaningful when turning a rail on. If level is omitted (or 0), SWD and JTAG are turned on without changing their currently selected voltage level, and VARV is turned on at its previously configured voltage.

Examples: Fixture Control (`TestPlanReference/fixture/`)
