# Programming Examples

Programming a target through a Test Agent and Flashr with `flashr-flash` (the main pattern), snippets for the built-in identify, erase and program commands, and a basic In-Circuit Test plan for the PLT demo board.

## flashr-flash - Program a target through Flashr

Source: `agentOS/flashr-flash/`

flashr-flash programs a firmware image into a target MCU through a Flashr PER-401 (`peripheral/prog/per-401/`) attached to the Test Agent. It is a wrapper around OpenOCD that drives the Flashr device as a CMSIS-DAP probe over SWD, writes the image, verifies it, and resets the target.

**Usage**

```
flashr-flash <target> <firmwareFile> [<offset>]
```

| Argument | Description |
|---|---|
| target | OpenOCD target name: the name of a configuration file in OpenOCD's target/ script directory, without the .cfg extension (for example nrf52 or stm32f4x). |
| firmwareFile | Path to the image to program. The image format is selected by the file extension (see below). |
| offset | Flash address to write the image to, for example 0x08000000. Required only for .bin files. |

**Image Formats**

The file extension decides how the image is handled:

- .bin is treated as a raw binary; an address offset is required.
- .hex or .elf — the load addresses come from the file itself, so offset must be omitted.

OpenOCD detects the image type based on the extension.

**Targets**

target must match a file named target/<target>.cfg in the OpenOCD script directory. Running flashr-flash with an unknown target name prints the list of available targets, which is a quick way to find the right name.

Set the OPENOCD_SCRIPTS environment variable to use a different script directory, for example to supply a custom target configuration sent to the Test Agent with agentCfg (`TestPlanReference/command/agentCfg/`).

**Programming sequence**

flashr-flash runs OpenOCD with fixed settings:

| Setting | Value |
|---|---|
| Debug adapter | CMSIS-DAP (interface/cmsis-dap.cfg) |
| Transport | SWD |
| Adapter speed | 4000 kHz |
| Program command | program <firmwareFile> [<offset>] verify reset exit |

The image is written, read back and verified, and the target is then reset to run the new firmware.

**Exit status**

| Status | Meaning |
|---|---|
| 0 | The image was programmed and verified. |
| 1 | The target name is unknown or the firmware file does not exist. |
| 2 | Usage error: wrong number of arguments, e.g., a .bin file without an offset or an offset given for another file type. |
| other | Exit status of OpenOCD, non-zero when the probe or target cannot be reached, or when programming or verification fails. |

Because the exit status reflects the result of the flashing operation, a failed agentExec (`TestPlanReference/command/agentExec/`) step is a reliable failure signal.

**Test plan example**

Send the image to the Test Agent with agentCfg (`TestPlanReference/command/agentCfg/`), then run flashr-flash with agentExec (`TestPlanReference/command/agentExec/`). Files listed under with: appear on the Test Agent in /run/pltagent/mnt.

```yaml
title: "Program DUT with Flashr"
suite:

 - title: "Setup Test Agent"
   steps:
    - command: agentCfg AGENT
      with:
       - firmware.hex

 - title: "Program DUT"
   steps:
    - command: agentExec AGENT "flashr-flash nrf52 /run/pltagent/mnt/firmware.hex"
      timeout: 2m
```

To program a raw binary, add the flash address:

```yaml
- command: agentExec AGENT "flashr-flash stm32f4x /run/pltagent/mnt/firmware.bin 0x08000000"
  timeout: 2m
```

> **NOTE:** We recommend that you set timeout: explicitly. The default agentExec timeout of 1000 ms may be shorter than your typical program-and-verify cycle.

**Limitations**

- SWD only; JTAG targets are not supported.
- The adapter speed is fixed at 4000 kHz.
- There is currently no option to select a probe, test agents should only be attached to a single Flashr device.

You can also drive the Flashr hardware with OpenOCD or pyOCD directly; see Blue Clover Flashr PER-401 (`peripheral/prog/per-401/`).

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
