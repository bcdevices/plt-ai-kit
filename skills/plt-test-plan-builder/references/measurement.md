# Electrical Measurements

How to measure voltage, current, resistance and frequency in a plan. Check `references/electrical-safety.md` before applying power.

## Electrical Measurements

Source: `TestPlanReference/measure/`

**Voltage**

Use the measure (`TestPlanReference/command/measure/`) command to test voltages on these PLT signals:

| channel | PLT Signal | Method | Max Voltage |
|---|---|---|---|
| voltageDATP00 | DATP00 | ADC | 5.5V |
| voltageDATP01 | DATP01 | ADC | 5.5V |
| voltageDATP02 | DATP02 | ADC | 5.5V |
| voltageDATP03 | DATP03 | ADC | 5.5V |
| voltageDATP04 | DATP04 | ADC | 5.5V |
| voltageDATP05 | DATP05 | ADC | 5.5V |
| voltageDATP06 | DATP06 | ADC | 5.5V |
| voltageDATP07 | DATP07 | ADC | 5.5V |
| voltageDATP08 | DATP08 | ADC | 5.5V |
| voltageDATP09 | DATP09 | ADC | 5.5V |
| voltageDATP10 | DATP10 | ADC | 5.5V |
| voltageDATP11 | DATP11 | ADC | 5.5V |
| voltageDATP12 | DATP12 | ADC | 5.5V |
| voltageDMM | DATPxx/DDTPxx | DMM | 100V |
| voltageMUX0 | MUX0 | ADC | 5.5V |
| voltageMUX1 | MUX1 | ADC | 5.5V |
| voltageMUX2 | MUX2 | ADC | 5.5V |
| voltageMUX3 | MUX3 | ADC | 5.5V |

> **CAUTION:** In order to avoid damage to the PLT, take care that signals are below the Max Voltage for the selected measurement channel.

*Example PLT test plan: Measure Voltages*

```yaml
title: "Measure Voltages"
suite:

- title: "Measure DATPxx Voltages"
  steps:
  # On the PLT-300A, it's necessary to connect DATP00 ... DATP06 to the mux before using voltageDATP00 ... voltageDATP06
  - command: mux connect DATP05
  - command: mux connect DATP06
  - command: measure voltageDATP05 3.1-3.4V
  - command: measure voltageDATP06 0.5-1.2V
  - command: measure voltageDATP07 200-3500mV
  - command: measure voltageDATP08 -0.2-0.1V
  - command: measure voltageDATP09 0-4V
  - command: measure voltageDATP10 -0.1-3.3V
  - command: measure voltageDATP11 0-3.4V
  - command: measure voltageDATP12 -0.1-3.4V

- title: "Measure MUXx Voltages"
  steps:
  - command: mux 0 DATP00
  - command: mux 1 DATP01
  - command: mux 2 RATP00
  - command: mux 3 RATP17
  - command: measure voltageMUX0 >1V
  - command: measure voltageMUX1 <3300mV
  - command: measure voltageMUX2 >100mV
  - command: measure voltageMUX3 1500-1800mV
```

Example: Use DMM to measure voltages >5V.

```yaml
title: "Measure High Voltages"
suite:

- title: "Measure"
  steps:
  # Check 24V rail, relative to GND4.
  - command: measure voltageDMM DATP00 22.8-25.2V
    ground: GND4
  # Check 12V rail, relative to PLT system GND.
  - command: measure voltageDMM DATP01 11-13V
```

**Commands**

- mux (`TestPlanReference/command/mux/`)
- measure (`TestPlanReference/command/measure/`)

**Voltage (differential)**

To measure differential voltage, use the measure (`TestPlanReference/command/measure/`) command with the voltageDiff channel and 2 signal names.

| channel | Method | Max Voltage |
|---|---|---|
| DATP00 | ADC | 5.5V |
| DATP01 | ADC | 5.5V |
| DATP02 | ADC | 5.5V |
| DATP03 | ADC | 5.5V |
| DATP04 | ADC | 5.5V |
| DATP05 | ADC | 5.5V |
| DATP06 | ADC | 5.5V |
| DATP07 | ADC | 5.5V |
| DATP08 | ADC | 5.5V |
| DATP09 | ADC | 5.5V |
| DATP10 | ADC | 5.5V |
| DATP11 | ADC | 5.5V |
| DATP12 | ADC | 5.5V |

Example: Measure differential voltage between DATP00 and DATP01

```yaml
title: "Measure differential (ADC)"
suite:
- title: "Measure"
  steps:
  - command: measure voltageDiff DATP00-DATP01 >100mV
```

The voltageDMM can also be used to perform differential measurements, by specifying a custom ground:.

| ground | Description | Max Voltage |
|---|---|---|
| GND | PLT System ground (default) | 5.5V |
| GND1 | DUT Ground #1 | 100V |
| GND2 | DUT Ground #2 | 100V |
| GND3 | DUT Ground #3 | 100V |
| GND4 | DUT Ground #4 | 100V |
| 1V8OUT | 1.8V supply | 1.8V |
| 3V3OUT | 3.3V supply | 3.3V |
| 5VOUT | 5V supply | 5.0V |
| VARVOUT | VARV supply | 24.5V |
| RVREF | RVREF mux signal | 5.5V |

Example: Use DMM to measure differential voltage.

```yaml
title: "Measure differential (DMM)"
suite:
- title: "Measure"
  steps:
  # Connect DATP00 to RVREF over MUX
  - command: mux 0 DATP01
  - command: mux 3 RVREF
  - command: short 0 3 set
  - command: mux connect DATP00
  # Measure DATP00 rail, relative to RVREF
  - command: measure voltageDMM DATP00 >100mV
    ground: RVREF
```

**Commands**

- mux (`TestPlanReference/command/mux/`)
- short (`TestPlanReference/command/short/`)
- measure (`TestPlanReference/command/measure/`)

**Current Draw**

Use the measure (`TestPlanReference/command/measure/`) command with current draw on these power rails:

| channel | Power Rail | Method |
|---|---|---|
| current1V8 | 1V8 | ADC |
| current3V3 | 3V3 | ADC |
| current5V | 5V | ADC |
| currentVARV | VARV | ADC |
| currentDMM | 1V8, 3V3, 5V, VARV, 12V, or 24V | DMM |

*Example PLT test plan: Measure Current Draw*

```yaml
title: "Measure Current Draw"
suite:
- title: "Measure Currents"
  steps:
  - command: measure current3V3 <1A
  - command: measure current5V 0.1-0.5A
  - command: measure currentVARV >100mA
  - command: measure currentDMM 1V8 <100mA
  - command: measure currentDMM 5V 0.1-0.5A
```

**Commands**

- mux (`TestPlanReference/command/mux/`)
- short (`TestPlanReference/command/short/`)
- sleepms (`TestPlanReference/command/sleepms/`)
- measure (`TestPlanReference/command/measure/`)

**Resistance**

To measure resistance, use the measure (`TestPlanReference/command/measure/`) command with the resistance or impedance channel.

The resistance channel measures resistance between the specified signal and the current system ground or a specified ground.

The impedance channel measures between the RA an RVREF PLT signals, which must be connected to the signals of interest, before performing the measurement.

We recommend using the resistance channel, unless compatibility with the PLT-200A is required.

*Example test plan: Measure Resistance*

```yaml
title: "Measure Resistance"
suite:
- title: "Measure Resistance"
  steps:
  # Measure resistance between DATP01 and system ground, with 5V reference
  - command: measure resistance DATP01 45-48kOhm 5V
  # Measure resistance between GND3 and DATP01
  - command: measure resistance DATP04 <50kOhm
    ground: GND3
  # Measure resistance between DATP02 and system ground, auto-ranging disabled.
  - command: measure resistance DATP02 9-11kOhm
    with:
      - disableAutoRange
```

*Example test plan: Measure Resistance*

```yaml
title: "Measure Resistance"
suite:
- title: "Measure Resistance"
  steps:
  - command: mux 0 RATP02
  - command: mux 1 RATP18
  - command: mux 2 RA
  - command: mux 3 RVREF
  - command: short 0 2 set
  - command: short 1 3 set
  - command: measure impedance 750-1000mOhm 3.3V
  - command: short 0 2 release
  - command: short 1 3 release
  - command: sleepms 1500
  - command: measure impedance 2-10Ohm 3300
```

**Commands**

- mux (`TestPlanReference/command/mux/`)
- short (`TestPlanReference/command/short/`)
- sleepms (`TestPlanReference/command/sleepms/`)
- measure (`TestPlanReference/command/measure/`)

**Capacitance**

To measure capacitance, use the measure (`TestPlanReference/command/measure/`) command with the capacitance channel.

The capacitance measurement will be performed between the specified signal and ground. If no ground is specified, the system ground will be used.

*Example PLT test plan: Measure Capacitance*

```yaml
title: "Measure Capacitance"
suite:
- title: "Measure Capacitance"
  steps:
  - command: ground 1
  - command: measure capacitance DATP01 <15nF
  - command: measure capacitance DDTP05 <150nF
  - command: measure capacitance DATP02 0.5-1.5uF
    ground: GND3
```

**Commands**

- measure (`TestPlanReference/command/measure/`)
- ground (`TestPlanReference/command/ground/`)

**Continuity**

To measure continuity, use the measure (`TestPlanReference/command/measure/`) command with the continuity channel.

Continuity is measured between the specified signal and ground. If no ground is specified, the system ground will be used.

*Example PLT test plan: Measure Continuity to Ground*

```yaml
title: "Measure Continuity to Ground"
suite:

- title: "Measure Continuity to Ground"
  steps:
  # Check continuity between DATP01 and system ground.
  - command: measure continuity DATP01 true
  # Check that there is no continuity between DDTP05 and system ground.
  - command: measure continuity DDTP05 false
  # Check continuity between DATP02 and GND3.
  - command: measure continuity DATP02 true
    ground: GND3
```

*Example PLT test plan: Measure Continuity DATP00 and DATP01*

```yaml
title: "Measure Continuity DATP00 and DATP01"
suite:

- title: "Measure Continuity DATP00 and DATP01"
  steps:
  # Route DATP00 to MUX0 and DATP01 to MUX1
  - command: mux 0 DATP00
  - command: mux connect DATP00
  - command: mux 1 RVREF
  # Connect MUX0 and MUX1
  - command: short 0 1 set
  # Check continuity between DATP01 and system ground.
  - command: measure continuity DATP01 true
    ground: RVREF
```

**Commands**

- measure (`TestPlanReference/command/measure/`)
- mux (`TestPlanReference/command/mux/`)
- short (`TestPlanReference/command/short/`)

**Digital**

Use the measure (`TestPlanReference/command/measure/`) command with the pin channel to test the value of digital inputs.

*Example PLT test plan: Digital pin measurements*

```yaml
title: "Digital pin measurements"
suite:
- ident: ICT-T1
  title: "Configure Digital pins as inputs"
  steps:
  - command: pin RDTP21 input pullup
  - command: pin DDTP04 input
- ident: ICT-T2
  title: "Read Digital pins"
  steps:
  - command: measure pin RDTP21 low
  - command: measure pin DDTP04 high
```

**Commands**

- pin (`TestPlanReference/command/pin/`)
- measure (`TestPlanReference/command/measure/`)
- mux (`TestPlanReference/command/mux/`)

**Frequency**

Use the measure (`TestPlanReference/command/measure/`) command with the frequency channel to test measure frequency.

The frequency measurement will be performed on either the CLK0 or CLK1 PLT signal, which must be selected with the freq (`TestPlanReference/command/freq/`) command, before performing the measurement.

*Example PLT test plan: Measure CLK0 frequency*

```yaml
title: "Measure CLK0 frequency"
suite:
- title: "Measure CLK0 frequency"
  steps:
  - command: freq 0
  - command: sleepms 1000
  - command: measure frequency 32.75-32.78kHz
```

*Example PLT test plan: Measure CLK1 frequency*

```yaml
title: "Measure CLK1 frequency"
suite:
- title: "Measure CLK1 frequency"
  steps:
  - command: freq 1
  - command: sleepms 1000
  - command: measure frequency 7.90-8.10MHz
```

Measure frequency with duty cycle.

> **NOTE:** Duty Cycle check only supported up to 60kHz.

*Example PLT test plan: Measure CLK1 frequency with Duty Cycle*

```yaml
title: "Measure CLK1 frequency"
suite:
- title: "Measure CLK1 frequency"
  steps:
  - command: freq 1
  - command: sleepms 1000
  - command: measure frequency 49.9-50.1KHz
    with:
    - dutyCycle 49-51%
```

**Commands**

- freq (`TestPlanReference/command/freq/`)
- measure (`TestPlanReference/command/measure/`)
- sleepms (`TestPlanReference/command/sleepms/`)

**Continuous Measurement**

The PLT can take continuous electrical measurements. Instead of a single measurement, signals are sampled continuously to evaluate mean, min, and max values over the sample period. This is particularly useful for characterizing a DUT with variable power consumption, such as a BLE or WiFi device.

Continuous Measurement is only available on the PLT-300A, and the measurement channel must support continuous measurement. Currently, the only supported continuous measurement channel is joulescope which requires a Joulescope JS220 (`peripheral/dmm/jetperch_joulescope_js220/`) connected to the PLT-300A.

*Example PLT test plan: Measure DUT Power Consumption for 10 seconds using Joulescope*

```yaml
title: "Measure DUT Power Consumption"
suite:
- title: "Measure DUT Power Consumption"
  steps:
  - command: measure start joulescope
    with:
    - voltageAverage:3-3.5V
    - voltageLimit:0-4V
    - currentAverage:10-20mA
    - currentLimit:0-100mA
    - powerAverage:30-50mW
    - powerLimit:0-100mW
  - command: sleepms 5000 "Measuring DUT power consumption..."
  - command: measure stop
```

**Commands**

- measure start and measure stop - Take continuous measurements over time.
- sleepms (`TestPlanReference/command/sleepms/`)
