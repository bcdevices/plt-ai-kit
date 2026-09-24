# Fixture Control

Driving the fixture from a plan: power rails and SWD/JTAG voltages, digital pins, mux routing and shorts, and ground select. On the PLT-300A, routing a probe through the mux caps it at 5.5V; check `references/electrical-safety.md` before applying power.

## Fixture Control

Source: `TestPlanReference/fixture/`

**Power Rails**

*Example PLT Test Plan: Power control*

```yaml
title: "Power control example"
suite:

- ident: ICT-T1
  title: "Apply power"
  steps:
  - command: power 3V3 on
  - command: power 5V on
  - command: power VARV 10.2

- ident: ICT-T2
  title: "Wait"
  steps:
  - command: sleepms 1000

- ident: ICT-T3
  title: "Power off"
  steps:
  - command: power off
```

*Example PLT Test Plan: Set SWD/JTAG voltages*

```yaml
title: "SWD/JTAG voltage control example"
suite:

- title: "SWD/JTAG voltages"
  steps:
  - command: power SWD 1.8
  - command: power JTAG 3.3
```

**Commands**

- power (`TestPlanReference/command/power/`)
- sleepms (`TestPlanReference/command/sleepms/`)

**Digital Pin Control**

*Example PLT Test Plan: Control digital pins*

```yaml
title: "Control digital pins"
suite:

# On the PLT-300A, it's necessary to connect DDTP00 ... DDTP08 to the mux before using them as digital pins.
# Caution: When connected to the mux, these pins maximum voltage is 5.5V.
- title: "Enable GPIO for digital pins"
  steps:
  - command: mux connect DDTP00
  - command: mux connect DDTP02
  - command: mux connect DDTP05
  - command: mux connect DDTP03
  - command: mux connect RDTP04

- title: "Configure digital inputs"
  steps:
  - command: pin DDTP05 input
  - command: pin DDTP03 input
  - command: pin RDTP04 input pullup

- title: "Control digital outputs"
  steps:
  - command: pin DDTP00 output high
  - command: pin DDTP02 output low
  - command: pin RDTP01 output high
  - command: pin SWD_NRST output low
  - command: pin UART1_RTS output high
```

**Commands**

- pin (`TestPlanReference/command/pin/`)
- mux (`TestPlanReference/command/mux/`)

**MUX Shorts**

*Example PLT Test Plan: Connect multiplex channels*

```yaml
title: "Multiplex example"
suite:

- title: "Control shorts"
  steps:
  - command: short 0 1 set
  - command: short 1 3 set
  - command: sleepms 1000

- title: "0-2 instead of 0-1"
  steps:
  - command: short 0 1 release
  - command: short 0 2 set
```

**Commands**

- short (`TestPlanReference/command/short/`)
- sleepms (`TestPlanReference/command/sleepms/`)

**MUX Select**

*Example PLT Test Plan: Multiplex control*

```yaml
title: "Multiplex control example"
suite:

- title: "Setup MUX"
  steps:
  - command: mux 0 DATP02
  - command: mux 1 DATP03
  - command: mux 2 RA
  - command: mux 3 RVREF
```

**Commands**

- mux (`TestPlanReference/command/mux/`)

**Ground Select**

*Example PLT Test Plan: Ground select*

```yaml
title: "Ground select"
suite:
- title: "Select GND2 as PLT system ground"
  steps:
  - command: ground 2
```
