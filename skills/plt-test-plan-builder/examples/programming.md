# Programming Examples

Snippets for identifying, erasing and programming a target, and a basic In-Circuit Test plan for the PLT demo board.

## Program Target Interaction

Source: `TestPlanReference/prog/`

**Program**

Example: Program NXP LPC11C24 over SWD, using built-in PLT programmer.

*Example PLT Test Plan: Program NXP LPC11C24 (SWD)*

```yaml
title: "NXP LPC11C24 (SWD)"
suite:
- title: "Power via SWD_VDD"
  steps:
  - command: power SWD on
- title: "Program firmware"
  steps:
  - command: program lpc11xx blinky.hex
```

- program (`TestPlanReference/command/program/`)

**Erase**

Example: Erase STM32L4 on-board flash, over the built-in SWD interface of the PLT.

*Example PLT Test Plan: Erase STM32L4 (SWD)*

```yaml
title: "Erase STM32L4 (SWD)"
suite:
- title: "Erase"
  steps:
  - command: erase STM32L4
```

**Commands**

- erase (`TestPlanReference/command/erase/`)

**Identify**

**Commands**

- identify (`TestPlanReference/command/identify/`)

## Basic Example

Source: `TestPlanReference/basic/`

A basic In-Circuit Test suite for the PLT demo board.

```yaml
title: "v0.1.8 (Green)"
identPrefix: "ICT-"
suite:

- ident: MCU
  title: "Identify, Erase and Program nRF52"
  steps:
  - command: identify nRF52
    title: "Identify DEMO-BOARD nRF52"
  - command: erase nRF52
    title: "Erase nRF52 Flash"
  - command: program nRF52 s132_nrf52_6.0.0_softdevice.hex,ly10-demo-fw-0.1.8.hex
    title: "Program DEMO-BOARD FW nRF52"

- ident: BLE
  title: "Detect DUT over BLE"
  steps:
  - command: bledis %BLEMAC% 30  # Wait up to 30 seconds for BLE discovery to complete
    title: "BLE discovery"
```
