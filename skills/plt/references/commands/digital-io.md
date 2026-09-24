# Digital I/O and signal routing

## mux

Multiplex Control

Hardware: PLT-300A

Control which signals are routed through the multiplex channels. This command is PLT-300A only.

There are two related but distinct operations:

- mux <channel> <signal> assigns a signal to one of the 4 multiplex channels (0..3), which then feeds into the ADC/DMM measurement paths for use with measure. Any signal previously assigned to that channel is replaced.
- mux connect|disconnect <signal> physically connects or disconnects a DATPxx/DDTPxx probe to/from the Multiplexer sub-system's relay matrix. A DDTPxx pin must be connected before it can be used as a GPIO (see pin); disconnect removes it from the mux again. A DATPxx pin (DATP00..``DATP06``) must likewise be connected before it can be measured as voltageDATP00..``voltageDATP06`` (see measure). all connects or disconnects every connectable signal at once.

```yaml
- command: mux <channel> <signal>

- command: mux connect|disconnect all|<signal>
```

| Argument | Description |
|---|---|
| `<channel>` | Multiplex channel index (0..``3``) to assign signal to. |
| `<connect>` | Connect signal (or all signals) to the Multiplexer sub-system's relay matrix. |
| `<disconnect>` | Disconnect signal (or all signals) from the Multiplexer sub-system's relay matrix. |
| `<signal>` | Probe or signal name, from the tables below. |
| `<all>` | All signals that can be connected to or disconnected from the multiplexer (see the second table below). |

_The following signals and probes can be assigned to a multiplex channel:_

| signal | MUX | Description |
|---|---|---|
| DATP00…DATP06 | 0, 1 | Direct Analog Test Probes |
| RATP00…RATP31 | 0, 1 | Routed Analog Test Probes |
| DDTP00…DDTP08 | 2, 3 | Direct Digital Test Probes |
| RVREF | all | Impedance measurement, reference voltage |
| RA | all | Impedance measurement, test voltage |
| GND | all | Ground |
| 1V8OUT | all | 1.8V power rail |
| 3V3OUT | all | 3.3V power rail |
| 5VOUT | all | 5.0V power rail |

_Since the multiplexer only tolerates up to 5V, the following signal probes can be connected or disconnected from the mux:_

| signal | Description |
|---|---|
| DATP00…DATP06 | Direct Analog Test Probes |
| DDTP00…DDTP08 | Direct Digital Test Probes |

> **WARNING:** The Multiplexer sub-system of the PLT only tolerates voltages up to 5.5V.

Examples: Fixture Control (`TestPlanReference/fixture/`), Electrical Measurements (`TestPlanReference/measure/`)
See also: `measure`, `pin`
## pin

Digital pin control

Configure a digital GPIO-capable probe as an input or output, and drive or read its logic level.

```yaml
- command: pin <probe> input [pullup|pulldown]

- command: pin <probe> output [low|high]
```

| Argument | Description |
|---|---|
| `<probe>` | Probe to configure. One of DDTPxx (Direct Digital Test Probe), RDTPxx (Routed Digital Test Probe), UART0_RTS/UART1_RTS, or SWD_NRST. |
| `input` | Configure the probe as an input, with the given pull configuration. |
| `pullup` | Enable the internal pull-up resistor on the pin. |
| `pulldown` | Enable the internal pull-down resistor on the pin. |
| `output` | Configure the probe as an output, driven to the given level. |
| `low` | Drive the output low (default if no level is given). |
| `high` | Drive the output high. |

If neither pullup nor pulldown is given for an input pin, the pin is left floating. UARTx_RTS and SWD_NRST only support output (they cannot be configured as inputs); read a digital signal's level instead with the measure command's pin channel.

> **NOTE:** On the PLT-300A, the DDTP00 ... DDTP08 pins need to be connected to the Multiplexer sub-system, to be used as GPIOs. Use the mux connect DDTPxx command to to connect such a pin to the Multiplexer sub-system.

> **WARNING:** When DDTPxx pins are connected to the Multiplexer sub-system, the maximum voltage is 5.5V.

Examples: Fixture Control (`TestPlanReference/fixture/`)
See also: `measure`, `mux`
## short

Connect Multiplex channels

Hardware: PLT-300A

Electrically connect (short) or disconnect two of the PLT-300A's four multiplexer channels to each other. This is used, for example, to route two signals that were each assigned to a mux channel with mux together, or to bridge two DUT test points through the multiplexer relay matrix. This command is PLT-300A only.

```yaml
- command: short <muxA> <muxB> set|release
```

| Argument | Description |
|---|---|
| `<muxA>` | Multiplex channel index (0..``3``). |
| `<muxB>` | Multiplex channel index (0..``3``), different from muxA. |
| `set` | Short (electrically connect) the two specified multiplex channels. |
| `release` | Release (disconnect) the short between the two specified multiplex channels. |

Examples: Fixture Control (`TestPlanReference/fixture/`)
See also: `mux`
