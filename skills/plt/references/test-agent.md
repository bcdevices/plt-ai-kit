# Test Agent (PER-101) and agentOS

The Test Agent's fixture setup and USB identity, and what agentOS provides to `agentExec`: the RAMDISK, the included tools and the shell environment. For `agentCfg` and `agentExec` syntax see `references/commands/agent.md`; for programming through a Flashr see `references/flashr.md`.

## Blue Clover Test Agent PER-101

Source: `peripheral/ta/per-101/`

The PLT Test Agent (PER-101) is a Raspberry Pi 4B-based SBC that runs agentOS (`agentOS/`). It provides a PLT-controllable suite of programming tools and other DUT interaction capabilities that are more naturally expressed as shell commands than as PLT primitives.

To the PLT, the Test Agent appears as a composite USB gadget with a USB-CDC console, a USB Mass Storage RAMDISK, and, from agentOS v2.0.2, a USB network interface. Test plans drive it with the agentCfg (`TestPlanReference/command/agentCfg/`) and agentExec (`TestPlanReference/command/agentExec/`) commands.

The tools available on the Test Agent are listed in agentOS (`agentOS/`).

**Fixture Setup**

- Connect the Test Agent's Type-C USB port to any of the PLT's peripheral Type-A USB ports, or to a USB hub attached to one of those ports. This single cable carries the USB-CDC console, the USB Mass Storage RAMDISK, and the USB network interface.
- Power the Test Agent externally, not from the PLT peripheral USB port.

**Default USB Identity**

The Test Agent enumerates with USB VID:PID 6666:8001. This is also the default that agentCfg (`TestPlanReference/command/agentCfg/`) resolves when id: is omitted, so most test plans do not need to specify it explicitly.

**Quickstart**

Configure the agent, transfer a script to its RAMDISK, and run it:

```yaml
title: "Test DUT with PLT Test Agent"
suite:
 - title: "Setup Test Agent"
   steps:
    - command: agentCfg TA
      with:
       - myscript.py

 - title: "Run script on Test Agent"
   steps:
    - command: agentExec TA "python3 /run/pltagent/mnt/myscript.py"
```

Files listed under with: land on the Test Agent at /run/pltagent/mnt.

**Examples**

Sample test plans that use a PLT Test Agent:

- flashr-flash - Program a target through Flashr (`agentOS/flashr-flash/`) — programming over SWD through a Flashr PER-401 (`peripheral/prog/per-401/`) with flashr-flash.
- Nordic nRF Util (`samples/ppcsbc/nordic-nrfutil/`) — Nordic nRF54 programming with nrfutil.
- Nordic nRF Command Line Tools (`samples/ppcsbc/nordic-nrfjprog/`) — Nordic nRF52 / nRF9160 modem programming with nrfjprog.
- Segger J-Link Software (`samples/ppcsbc/segger-commander/`) — Segger J-Link Commander.
- Segger Flasher Software (`samples/ppcsbc/segger-flasher-software/`) — Segger Universal Flasher and FlasherControl.
- NXP Secure Provisioning SDK (`samples/ppcsbc/nxp-spsdk/`) — NXP Secure Provisioning SDK.
- RPi Camera Module (`samples/ppcsbc/rpi-camera/`) — Camera capture with libcamera.

## agentOS

Source: `agentOS/`

agentOS is Blue Clover's Linux distribution for the Blue Clover Test Agent PER-101 (`peripheral/ta/per-101/`) that acts alongside a PLT during production testing. agentOS exposes a USB-CDC console, a USB Mass Storage RAMDISK, and a USB network interface. The PLT drives it with the agentCfg (`TestPlanReference/command/agentCfg/`) and agentExec (`TestPlanReference/command/agentExec/`) commands.

**Capabilities**

An agentOS image presents itself to the PLT as a composite USB gadget:

- USB-CDC console (/dev/ttyGS0 on the SBC) — 1,000,000 baud 8N1, with autologin as the pltagent user. Any shell command issued with agentExec (`TestPlanReference/command/agentExec/`) runs on the Test Agent.
- USB Mass Storage RAMDISK — files sent from the PLT with agentCfg's with: list appear on the SBC at /run/pltagent/mnt, so a test plan can hand firmware images, archives, or scripts to Test Agent for execution. The RAMDISK is 256 MB and FAT16-formatted.
- USB network interface — a USB Ethernet (CDC-ECM) function with link-local addressing. See USB network interface.

Build info (/etc/buildinfo) is reported back to the PLT so the agent's DISTRO_VERSION shows up alongside test results.

**USB identity**

| USB descriptor | Value |
|---|---|
| VID:PID | 6666:8001 |
| Manufacturer | Blue Clover Devices |
| Product | per-101 running: <distro> ver: <version> |
| Serial number | The Test Agent's board serial number |

**USB network interface**

The Test Agent presents a USB Ethernet (CDC-ECM) function next to the console and the RAMDISK. All three are part of the same USB configuration, so test plans that use the console and RAMDISK keep working unchanged.

- On the Test Agent the interface is named usb0.
- usb0 is configured with link-local addressing for both IPv4 (169.254.0.0/16) and IPv6 (fe80::/10).
- The Test Agent announces itself with mDNS on usb0 only, as per101-<serial>.local, where <serial> is the board serial number that is also reported as the USB serial number.

The board serial number is available in a console session as the OTP_ID environment variable:

```console
$ echo "per101-${OTP_ID}.local"
```

**Included tools**

The tools below are part of the agentOS image as of agentOS v2.0.3 and can be run with agentExec (`TestPlanReference/command/agentExec/`) without installing anything.

**Blue Clover commands**

| Command | Purpose |
|---|---|
| flashr-flash (`agentOS/flashr-flash/`) | Program a .hex, .elf, or .bin image into a target through an attached Flashr (`peripheral/prog/per-401/`). |
| flashr-update (`agentOS/flashr-update/`) | Upload a firmware update to an attached Flashr. |
| pltagent-msc-present, pltagent-msc-mount | Detect and mount a USB Mass Storage device exposed by a DUT. See NXP i.MX RT685 EVK (`samples/board/mimxrt685_evk/`) and Microchip Explorer 16/32 (`samples/board/mcpexplorer16_32/`) for worked examples. |
| pltagent-cam [auto\|fixed] [<outputFile>] | Capture a still image with libcamera-still. auto (default) uses automatic exposure and gain; fixed uses a fixed shutter time, gain, and white balance for repeatable captures. The image is written to /tmp/capture.jpg unless outputFile is given. |
| nrf52_flash.py | Recover, erase, program, verify, and reset an nRF52 through nrfutil. Options include --hex <file>, --recover, --erase, --verify, and --sn <serialNumber>. The last line of output is always nrf52_flash:DONE:<exitCode>:<message>. |
| led-act on\|off, led-pwr on\|off | Switch the Test Agent's ACT and PWR LEDs, for example as an operator indicator. Run with sudo. |

**Vendor tools**

| Command | Notes |
|---|---|
| nrfutil | Nordic nRF Util with the device command installed. The command on the path is a wrapper that always passes --json --log-output stdout, so output reaches the console. See Nordic nRF Util (`samples/ppcsbc/nordic-nrfutil/`). |
| JLinkExe | SEGGER J-Link Commander V9.16a, also available as /opt/SEGGER/JLink/JLinkExe. See Segger J-Link Software (`samples/ppcsbc/segger-commander/`). |

**Open-source tools**

| Purpose | Tools |
|---|---|
| Programming | openocd, stm32flash, flashrom, mcumgr, rpiboot, mtd-utils, srecord |
| Buses and I/O | i2c-tools, spitools, canutils, picocom, sigrok-cli, mbpoll, pymodbus (Python) |
| Display and camera | edid-decode, read-edid, libcamera-apps |
| Storage | parted, dosfstools, squashfs-tools, blkid |
| Network | atftp, dnsmasq, usbip, openssh |
| System | lsusb, lshw, vcgencmd, vcmailbox, rpi-eeprom, python3 |

**Environment**

- Commands run as the pltagent user. sudo works without a password.
- The root file system is read-only. Write temporary files to /tmp or to the RAMDISK at /run/pltagent/mnt; to install additional software, remount the root file system read-write first, as shown in Segger J-Link Software (`samples/ppcsbc/segger-commander/`).

**Usage**

An agentOS SBC is set up with agentCfg (`TestPlanReference/command/agentCfg/`), then any command line is executed on it with agentExec (`TestPlanReference/command/agentExec/`). The default USB VID:PID for an agentOS device is 6666:8001.

```yaml
title: "Test DUT using an agentOS SBC"
suite:

 - title: "Setup SBC"
   steps:
    - command: agentCfg AGENT
      with:
       - myscript.py

 - title: "Power DUT"
   steps:
    - command: ground all
    - command: power 3V3 on

 - title: "Test DUT with SBC"
   steps:
    - command: agentExec AGENT "python3 /run/pltagent/mnt/myscript.py"
```

**Examples**

Sample test plans that exercise agentOS:

- Nordic nRF Util (`samples/ppcsbc/nordic-nrfutil/`) — nRF54 programming with nrfutil, plus an SD-card preparation plan.
- Nordic nRF Command Line Tools (`samples/ppcsbc/nordic-nrfjprog/`) — nRF52 / nRF9160 modem programming with nrfjprog.
- Segger J-Link Software (`samples/ppcsbc/segger-commander/`) — J-Link Commander for EFM32 programming.
- Segger Flasher Software (`samples/ppcsbc/segger-flasher-software/`) — SEGGER Universal Flasher / FlasherControl.
- NXP Secure Provisioning SDK (`samples/ppcsbc/nxp-spsdk/`) — NXP Secure Provisioning SDK (sdphost).
- Console (`samples/linux/console/`) — patterns for parsing DUT/SBC UART output.
