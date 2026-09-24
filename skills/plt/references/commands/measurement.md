# Measurement

## eval

Evaluate Expression

Evaluate an expression and use its result as the step's pass/fail outcome and result value.

```yaml
- command: eval <expression>
  [extractKey: <key>]
```

| Argument | Description |
|---|---|
| `<expression>` | Expression to evaluate |
| `<key>` | Key in which to store the evaluated expression value |

expression may reference any key set with define, plus a fixed set of system keys (PRODUCT, VERSION, BOM_REV, DUT_ID, SERIAL_NUMBER, PLT_RUNNER_VERSION, PLT_OS_VERSION, TEST_PLAN_TITLE, PLT_IP_ADDRESS, RELEASE_UUID, PROJECT_UUID) and any key extracted by a prior value, measure, or similar step. A key set with define overrides a system key of the same name. Reference a key by its bare name inside expression (e.g. SERIAL_NUMBER == "12345"); use %KEY% substitution only where the key must be expanded before the expression is parsed, such as inside a regular expression literal.

The step's outcome depends on the type of the evaluated result:

- A boolean result of true passes the step; false fails it.
- A non-empty string or numeric result passes the step, and becomes the result value (stored under key if extractKey: is set).
- An empty string result fails the step.

_Supported operators:_

| Operator | Description |
|---|---|
| + | Addition, concatenation |
| - | Subtraction, Negation |
| / | Division |
| * | Multiplication |
| ** | Power |
| % | Modulo |
| & | Bitwise And |
| \| | Bitwise Or |
| ^ | Bitwise Xor |
| ~ | Bitwise Not |
| >> | Right shift |
| << | Left shift |
| ! | Inversion |
| && | Logical And |
| \|\| | Logical Or |
| ? | Ternary True |
| : | Ternary False |
| ?? | Null coalescence |
| > | Greater than |
| < | Less than |
| <= | Less than or equal |
| >= | Greater than or equal |
| == | Equal |
| != | Not equal |
| =~ | Regex match |
| !~ | Regex mismatch |
| in | Set membership, e.g. "a" in ("a", "b", "c") |

_Supported functions:_

| Function | Description |
|---|---|
| bytes(val1 [, val2] [, ...]) | Build a string from one or more numeric byte values (each argument is truncated to a byte, 0-255). |
| hex(value) | Convert numeric value to a hexadecimal string (no leading 0x). |
| numeric(value [, unit]) | Convert value to a numeric value. value may be a bool, number, numeric string, or a measurement result (voltage, current, resistance, power, or frequency). Optional unit (e.g. mV, mA, kOhm) scales a measurement result before returning it as a plain number. |
| utcTime([format [, timezone]]) | Returns the current timestamp. If format is provided, the date is returned in the specified format using Golang Time Format; otherwise it defaults to YYYY-MM-DD. If timezone is provided (an IANA time zone name, e.g. America/Los_Angeles), the timestamp is rendered in that zone instead of UTC. |

Examples: Keys (`TestPlanReference/keys/`), Label Printing (`TestPlanReference/barprint/`)
See also: `value`
## freq

Frequency Monitor Control

Select which clock input signal (CLK0 or CLK1) the PLT's frequency counter reads. This only selects the input; it does not take a measurement. Follow it with a measure step using the frequency channel to actually read and check the frequency (and, on the PLT-300A, duty cycle) of the selected signal.

```yaml
- command: freq 0|1
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `0` | Use CLK0 as the frequency measurement input. |
| `1` | Use CLK1 as the frequency measurement input. |
| `<retryCount>` | Number of times to retry the test step (optional). |

Examples: Electrical Measurements (`TestPlanReference/measure/`)
See also: `measure`
## measure

Probe Measurement

### `measure <channel>`

In this usage, the measure command is used to take a measurement of a signal using a particular measurement channel. The PLT takes a single reading on the selected channel, compares it against the pass/fail criteria given by range/acceptance (if any), and reports the numeric result. Use freq beforehand to select which clock input the frequency channel reads, and mux beforehand for any signal that must first be routed through the Multiplexer sub-system on the PLT-300A.

```yaml
- command: measure <channel> [<signal>|<rail>] <range>|<acceptance> [<reference>]
  [extractKey: <key>]
  [retry: <retryCount>]
  [ground: <ground>]
  [with:
    [- dutyCycle <dutyCycleRange>]
    [- disableAutoRange]]
```

| Argument | Description |
|---|---|
| `<channel>` | Measurement channel to use, from the table below. |
| `<signal>` | The probe or signal to measure: a DDTPxx/RDTPxx probe for the pin channel, or a DATPxx/DDTPxx probe (or RA) for a DMM-based measurement. Not used for impedance (always measures RA), the currentDMM channel (which instead takes a power rail name), or any channel whose name already identifies a fixed signal — the ADC current channels (current1V8, current3V3, current5V, currentVARV), the voltageDATP00.. voltageDATP12 channels, and the voltageMUX0.. voltageMUX3 channels. |
| `<rail>` | Power rail name for currentDMM measurement (e.g. 3V3, 5V, VARV). See power. |
| `<range>` | Acceptable numeric range for the measured quantity, e.g. 3.2-3.4V, <100mA, or >1kOhm. See the suffix table below for supported units. A bare min-max range (min-max) or an open-ended range using <max or >min is accepted; omitting the range applies no pass/fail criteria (the reading is always logged). |
| `<acceptance>` | Signal acceptance criteria: a range for numeric channels, low or high for the pin channel, or a boolean (True/False/1/0) for the continuity channel. |
| `<reference>` | Reference voltage for impedance and resistance measurements (optional, default: 5V). |
| `<key>` | Key in which to store the measurement result, for later use with eval or label substitution (optional). |
| `<retryCount>` | Number of times to retry the test step (optional). |
| `<ground>` | Measurement reference ground signal (optional, default: GND). See the ground table below. PLT-300A only. |
| `<with>` | Additional command parameters. (optional) disableAutoRange - Turn off DMM auto-ranging for this measurement. Available for currentDMM, resistance, and voltageDMM channels. dutyCycle - Duty cycle range for frequency measurement. Available for frequency channel, only on PLT-300A. |

A range or reference value that omits a unit suffix defaults to the base unit for its quantity (V for voltage, A for current, Ohm for resistance/impedance, Hz for frequency).

For DMM-based measurements, the PLT-300A allows measurements to be taken against a specific ground signal. This can be requested by adding a ground: <ground> field to the measure command, with the following supported values:

### `measure start and measure stop`

In this usage of the measure command, the start and stop subcommands are used to start a continuous measurement, and then stop it.

This functionality is only available on the PLT-300A, and the specified channel must support continuous measurement.

Other commands can be used between start and stop to wait for measurement (e.g., sleepms), or to exercise the DUT (e.g., power, GPIO, etc). Measurements will be taken continuously, and results will be tested against the pass criteria specified in the start command when stop is called.

Multiple continuous measurements can be started and stopped in parallel, as long as they are on separate channels.

```yaml
- command: measure start <channel>
  [id: <usbDeviceID>]
  [path: <usbDevicePath>]
  [retry: <retryCount>]
  [with:
    [- voltageAverage:<voltageAverageRange>]
    [- voltageLimit:<voltageLimitRange>]
    [- currentAverage:<currentAverageRange>]
    [- currentLimit:<currentLimitRange>]
    [- powerAverage:<powerAverageRange>]
    [- powerLimit:<powerLimitRange>]]

- command: measure stop [<channel>]
  [id: <usb_device_id>]
  [path: <usb_device_path>]
```

| Argument | Description |
|---|---|
| `<channel>` | Measurement channel. Note: The selected channel must support continuous measurement. Defaults to joulescope if omitted. |
| `<usb_device_id>` | Optional: USB device identifiers: VID:PID. Use to disambiguate when more than one matching USB peripheral is attached. |
| `<usb_device_path>` | Optional: USB device path: port. ... .port. Use to disambiguate when more than one matching USB peripheral is attached. |
| `<retryCount>` | Optional: Number of times to retry the test step. |
| `<with>` | Optional: Additional command parameters. (Note: If none of the parameters below are specified, no pass criteria will be applied.) |
| `<voltage_average_range>` | Optional: Acceptable range for the average voltage over the capture. |
| `<voltage_limit_range>` | Optional: Acceptable range for the minimum and maximum instantaneous voltage seen during the capture. |
| `<current_average_range>` | Optional: Acceptable range for the average current over the capture. |
| `<current_limit_range>` | Optional: Acceptable range for the minimum and maximum instantaneous current seen during the capture. |
| `<power_average_range>` | Optional: Acceptable range for the average power over the capture. |
| `<power_limit_range>` | Optional: Acceptable range for the minimum and maximum instantaneous power seen during the capture. |

measure start begins a continuous capture on the given peripheral; measure stop ends the capture and evaluates the average/limit criteria supplied to measure start against the average, minimum, and maximum voltage, current, and power observed during the capture.

_The measure command supports the following channels:_

| channel | Description | Max Voltage |
|---|---|---|
| capacitance | Capacitance, using DMM | 100V |
| continuity | Continuity, using DMM | 100V |
| current1V8 | 1V8 power rail current draw, using ADC | 5.5V |
| current3V3 | 3V3 power rail current draw, using ADC | 5.5V |
| current5V | 5V power rail current draw, using ADC | 5.5V |
| currentVARV | VARV power rail current draw, using ADC | 24V |
| currentDMM | Current on a power rail, using DMM | 100V |
| frequency | Frequency on the channel set by freq | 100V |
| impedance | Impedance of RA vs. RVREF | 100V |
| pin | Digital pin measurement (DDTPxx/RDTPxx) | 5.5V |
| resistance | Resistance, using DMM | 100V |
| voltageDATP00 | DATP00 voltage, using ADC | 5.5V |
| voltageDATP01 | DATP01 voltage, using ADC | 5.5V |
| voltageDATP02 | DATP02 voltage, using ADC | 5.5V |
| voltageDATP03 | DATP03 voltage, using ADC | 5.5V |
| voltageDATP04 | DATP04 voltage, using ADC | 5.5V |
| voltageDATP05 | DATP05 voltage, using ADC | 5.5V |
| voltageDATP06 | DATP06 voltage, using ADC | 5.5V |
| voltageDATP07 | DATP07 voltage, using ADC | 5.5V |
| voltageDATP08 | DATP08 voltage, using ADC | 5.5V |
| voltageDATP09 | DATP09 voltage, using ADC | 5.5V |
| voltageDATP10 | DATP10 voltage, using ADC | 5.5V |
| voltageDATP11 | DATP11 voltage, using ADC | 5.5V |
| voltageDATP12 | DATP12 voltage, using ADC | 5.5V |
| voltageDiff | Differential voltage, using ADC | 5.5V |
| voltageDMM | Voltage, using DMM | 100V |
| voltageMUX0 | MUX0 voltage, using ADC | 5.5V |
| voltageMUX1 | MUX1 voltage, using ADC | 5.5V |
| voltageMUX2 | MUX2 voltage, using ADC | 5.5V |
| voltageMUX3 | MUX3 voltage, using ADC | 5.5V |

_ADC-based differential voltage measurements (voltageDiff) are supported for the following combinations of signals only:_

| signal | signal |
|---|---|
| DATP00 | DATP01 |
| DATP00 | DATP03 |
| DATP01 | DATP03 |
| DATP02 | DATP03 |
| DATP04 | DATP05 |
| DATP04 | DATP07 |
| DATP05 | DATP07 |
| DATP06 | DATP07 |
| DATP08 | DATP09 |
| DATP08 | DATP11 |
| DATP09 | DATP11 |
| DATP10 | DATP11 |

_DMM-based measurements (capacitance, continuity, currentDMM, resistance, voltageDMM) can be performed for the following probes:_

| signal | Description |
|---|---|
| DATP00…DATP06 | Direct Analog Test Probe #0…#6 |
| DDTP00…DDTP08 | Direct Digital Test Probe #0…#8 |
| RA | RA MUX signal |

| ground | Description |
|---|---|
| GND | PLT System ground (default) |
| GND1 | DUT Ground #1 |
| GND2 | DUT Ground #2 |
| GND3 | DUT Ground #3 |
| GND4 | DUT Ground #4 |
| 1V8OUT | 1.8V supply |
| 3V3OUT | 3.3V supply |
| 5VOUT | 5V supply |
| VARVOUT | VARV supply |
| RVREF | RVREF mux signal |

_The following suffixes are supported for electrical measurement ranges:_

| Kind | Suffix | Description |
|---|---|---|
| Frequency | Hz | Hertz (default) |
| Frequency | kHz, KHZ | Kilohertz |
| Frequency | MHz | Megahertz |
| Frequency | GHz | Gigahertz |
| Voltage | nV | Nanovolt |
| Voltage | uV, µV | Microvolt |
| Voltage | mV | Millivolt |
| Voltage | V | Volt (default) |
| Voltage | kV, KV | Kilovolt |
| Voltage | MV | Megavolt |
| Current | nA | Nanoampere |
| Current | uA, µA | Microampere |
| Current | mA | Milliampere |
| Current | A | Ampere (default) |
| Resistance/Impedance | nOhm | Nanoohm |
| Resistance/Impedance | uOhm, µOhm | Microohm |
| Resistance/Impedance | mOhm | Milliohm |
| Resistance/Impedance | Ohm | Ohm (default) |
| Resistance/Impedance | kOhm, KOhm | Kiloohm |
| Resistance/Impedance | MOhm | Megaohm |

_The following channels are supported for continuous measurement:_

| channel | Description |
|---|---|
| joulescope | Jetperch Joulescope JS220 Precision Energy Analyzer. External USB peripheral. Supports continuous measurement of voltage, current, and power. |

> **NOTE:** For the voltageDiff channel, 2 signal names must be provided, separated with a -. For example: DATP00-DATP01 for a differential measurement between DATP00 and DATP01.

> **NOTE:** For the continuity channel, acceptance is a boolean value (True/False, 1/0, t/f) indicating whether continuity is expected between signal and ground.

> **CAUTION:** In order to avoid damage to the PLT, take care that signals are below the Max Voltage for the selected measurement channel.

> **NOTE:** On the PLT-300A, the DATP00 ... DATP06 pins need to be connected to the Multiplexer sub-system, in order to use voltageDATP00 ... voltageDATP06. Use the mux connect DDTPxx command to to connect such a pin to the Multiplexer sub-system.

Examples: Electrical Measurements (`TestPlanReference/measure/`), Jetperch Joulescope JS220 (`peripheral/dmm/jetperch_joulescope_js220/`)
See also: Electrical Safety (`TestPlanReference/electrical-safety/`), PLT-300A Reference (`plt-300a/`), Probes and Signals (`plt-300a/signals/`)
## value

Parse values

Extract data from a value.

```yaml
- command: value <payloadText>
  [expect: [hex] <expectText>]
  [extract: <extractText>]
  [extractKey: <key>...]
```

| Argument | Description |
|---|---|
| `<payloadText>` | Value to check and/or extract from. |
| `<expectText>` | Text that must appear anywhere in payloadText (substring match), checked before extraction; the step fails if it is not found. If the hex keyword is used, expectText is decoded from a hex string and the raw bytes are matched instead. |
| `<extractText>` | Regular expression to extract (uses RE2 Syntax, except \C) |
| `<key>` | Key(s) in which to store extracted text. To save multiple values, use multiple capture groups. |

With no expect: or extract:, the step passes and its result value is payloadText unchanged. If extract: is given but the regular expression does not match payloadText, the step fails.

extractKey: values are assigned to capture groups positionally (the first key gets the first capture group, and so on) and stored as test plan keys, the same store used by define — making them usable by later eval or label steps. If more keys are given than the regular expression has capture groups, the step fails.

```yaml
# Extract 2 capture groups
- command: define TEXT "Foobar1234"
- command: value "%TEXT%"
  extract: "^(\\D+)(\\d+)$"
  extractKey: ALPHA DIGITS
```

```yaml
# Match hex values
- command: value "ABC"
  expect: hex 414243
```

See also: `eval`, `uart`
