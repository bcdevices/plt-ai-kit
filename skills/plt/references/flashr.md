# Flashr (PER-401)

Programming a DUT through a Flashr attached to a Test Agent: the `flashr-flash` and `flashr-update` commands run with `agentExec`, and driving a Flashr directly with OpenOCD or pyOCD. For the Test Agent itself see `references/test-agent.md`.

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

## flashr-update - Update Flashr firmware

Source: `agentOS/flashr-update/`

flashr-update programs a flashOS (`releases/flashOS/`) firmware image to a Flashr PER-401 (`peripheral/prog/per-401/`) attached to the Test Agent. It is a wrapper around mcumgr, which transfers the image over the Flashr's firmware update serial port.

**Usage**

```
flashr-update
```

The command takes no arguments. It looks for the firmware image by name, in this order, and uploads the first match:

1. /var/lib/pltagent/per401-fw-*
2. /run/pltagent/mnt/per401-fw-*

The second location is the RAMDISK, so an image sent with agentCfg (`TestPlanReference/command/agentCfg/`) is found without further setup.

**Firmware image**

Send the signed application image of the flashOS release, named per401-fw-v<version>-slot0.signed.bin.

> **WARNING:** Any file whose name starts with per401-fw- matches, and only the first match is used. Send exactly one such file.

**Flashr serial port**

agentOS creates the device link /dev/flashr-<serial>-serial for the serial port of an attached Flashr, where <serial> is the Flashr's USB serial number. flashr-update uses this link. The software expects a single Flashr to be attached to the Test Agent.

**Activating the update**

flashr-update only programs the image into the Flashr's alternate firmware slot. The Flashr keeps running its current firmware until the uploaded image is marked for use and the Flashr is restarted:

```console
$ CONN="dev=$(echo /dev/flashr*-serial),baud=115200"
$ mcumgr --conntype serial --connstring "$CONN" image list
$ mcumgr --conntype serial --connstring "$CONN" image test <hash>
$ mcumgr --conntype serial --connstring "$CONN" reset
```

image list reports the hash of the image in slot 1.

After the restart, the bootloader verifies the image signature and starts the new firmware. If the new firmware does not confirm itself, the Flashr reverts to the previous firmware on the next restart.

**Exit status**

| Status | Meaning |
|---|---|
| 0 | The image was uploaded. |
| 1 | No firmware image was found. |
| other | Exit status of mcumgr, non-zero when the Flashr cannot be reached or the upload fails. |

**Test plan example**

```yaml
title: "Update Flashr firmware"
suite:

 - title: "Setup Test Agent"
   steps:
    - command: agentCfg AGENT
      with:
       - per401-fw-v0.6.0-slot0.signed.bin

 - title: "Upload Flashr firmware"
   steps:
    - command: agentExec AGENT "flashr-update"
      timeout: 2m
```

## Blue Clover Flashr PER-401

Source: `peripheral/prog/per-401/`

The Flashr (PER-401) is Blue Clover's USB programming device. It runs flashOS (`releases/flashOS/`). Flashr presents itself as a CMSIS-DAP probe, so it is driven with standard CMSIS-DAP tooling to program and debug a target over SWD.

**Program a target from a Test Agent**

In a test station, attach the Flashr to a Test Agent (`peripheral/ta/per-101/`) and program the target with the flashr-flash command included in agentOS (`agentOS/`):

```yaml
- command: agentExec AGENT "flashr-flash nrf52 /run/pltagent/mnt/firmware.hex"
  timeout: 2m
```

See flashr-flash - Program a target through Flashr (`agentOS/flashr-flash/`) for the arguments, exit status, and a complete test plan.

**Use the Flashr directly**

flashr-flash is a wrapper around OpenOCD. The Flashr can also be driven directly, from a Test Agent or from a development computer, with any debug host that supports CMSIS-DAP. This is how to reach what flashr-flash does not offer, such as a different adapter speed or a debugger connection.

The examples below use rp2350 as the target; substitute the name of your target.

**OpenOCD**

> **NOTE:** OpenOCD needs a valid configuration file for the target. Some targets are not shipped with OpenOCD 0.12 by default, such as the RP2350. For RP2350 targets use a more recent build or the Raspberry Pi fork (https://github.com/raspberrypi/openocd).

Check the connection to the target. A successful connect reads the target's DPIDR and examines its cores:

```console
$ openocd -f interface/cmsis-dap.cfg -c "transport select swd" \
          -c "adapter speed 4000" -f target/rp2350.cfg -c "init" -c "exit"
```

Program an image with the program command, which erases, writes, verifies, and resets. For .elf and .hex files the load addresses are contained within the file and do not need to be specified:

```console
$ openocd -f interface/cmsis-dap.cfg -c "transport select swd" \
          -c "adapter speed 4000" -f target/rp2350.cfg \
          -c "program firmware.elf verify reset exit"
```

A raw .bin file needs the load address, for example the RP2350 flash base:

```console
$ openocd -f interface/cmsis-dap.cfg -c "transport select swd" \
          -c "adapter speed 4000" -f target/rp2350.cfg \
          -c "program firmware.bin 0x10000000 verify reset exit"
```

**pyOCD**

pyOCD has built-in RP2350 support and needs no target configuration files. It is not included in agentOS at this time, but can be used from a development machine. An attached Flashr device is listed as flashOS CMSIS-DAP:

```console
$ pip3 install pyocd
$ pyocd list
```

Program an .elf, .hex, or .bin image:

```console
$ pyocd flash -t rp2350 firmware.elf
```

**Update the Flashr firmware**

A Flashr attached to a Test Agent is updated with the flashr-update command included in agentOS (`agentOS/`).

```yaml
- command: agentCfg AGENT
  with:
   - per401-fw-v0.6.0-slot0.signed.bin
- command: agentExec AGENT "flashr-update"
  timeout: 2m
```

See flashr-update - Update Flashr firmware (`agentOS/flashr-update/`) for details, including how the uploaded image is activated.
