# Bento Board

The example DUT: its firmware, repositories, wiring, and test plans.

## Bento Board

Source: `samples/board/bento/`

- Vendor: Blue Clover Devices
- Bento Board (PLT demo board v3)
- Program Target: Raspberry Pi RP2350B (Cortex-M33)

The Bento Board is a demo harware target for Blue Clover's "postcard demo": a small, self-contained example that exercises the Blue Clover hardware end-to-end:

- PLT-106 (`plt-106/`) runs the test plan and powers the DUT
- PER-101 Test Agent (`peripheral/ta/per-101/`) facilitates the use of programming, fixture control, and software tools.
- A debug probe (Flashr PER-401 (`peripheral/prog/per-401/`), or a SEGGER J-Link) programs the RP2350B over SWD
- The Bento Board is the Device Under Test (DUT)

**Peripherals**

Bento peripherals: RP2350B MCU, ESP32-C3 RF SoC, addressable RGB LEDs (WS2812), buzzer, 5 V relay, environmental sensor (BME280), Qwiic, mikroBUS, and USB Type-C.

**Repositories**

| Repository | Contents |
|---|---|
| bcdevices/bento-zephyr-fw (https://github.com/bcdevices/bento-zephyr-fw) | Zephyr firmware: app (demo application) and blinky, both with a shell; board definitions under boards/blueclover/. Prebuilt Bento images are on the releases page (https://github.com/bcdevices/bento-zephyr-fw/releases). |
| bcdevices/test-plans (https://github.com/bcdevices/test-plans) | Example YAML test plans under bento/, including bento-flashr-blinky.yaml |
| bcdevices/example-projects (https://github.com/bcdevices/example-projects) | Hardware design files and a test plan in bento-board/ |

To build locally (see the repository README.md for toolchain setup):

```shell
make app BOARD=bento
make blinky BOARD=bento
make docker                # containerized build, output in dist/
```

Images are written to build.<board>/rp2350b/m33/{app,blinky}/zephyr/zephyr.hex.

**Verifying the image**

The app image exposes a Zephyr shell over USB CDC-ACM (prompt bento:~$). Query the version with:

```shell
bento:~$ app version
bento:~$ app build-version
```

The blinky image also exposes a Zephyr shell over USB CDC-ACM (prompt blinky:~$). Query the application, build, Zephyr, and board versions with:

```shell
blinky:~$ version
```

**Program Bento Board with J-Link**

**Test Station**

| SKU | Model No. | Model Name |
|---|---|---|
| SKU-6 | PLT-106 | Production Line Tool |
| SKU-7 | PER-101 | Test Agent |
| — | J-Link Base Compact | J-Link Programmer |
| SUB-67 | Bento Board | Device Under Test |

**Connection**

| Device A | Connector | Cable P/N | Connector | Device B |
|---|---|---|---|---|
| SKU-6 | USB-A (Port 1) | TBD | USB-C (PLT port) | SKU-7 |
| SKU-7 | USB-A (Port 2) | TBD | USB-B | J-Link Base Compact |
| J-Link Base Compact | 20-pin Header | TBD | J1 Tag-Connect | SUB-67 |
| SKU-6 | USB-A (Port 2) | TBD | USB-C | SUB-67 |

**YAML test plan**

Program the RP2350B with bento_blinky.hex, available from the v1.0.1 firmware release (https://github.com/bcdevices/bento-zephyr-fw/releases/tag/v1.0.1). Add bento_blinky.hex to the PLTcloud project alongside the test plan.

```yaml
title: "Bento Flashing Demo"
description: "Flash RP2350B via PER-101 Test Agent and J-Link Commander"

suite:

  - title: "Defines"
    steps:
      - command: define FIRMWARE "bento_blinky.hex"
      - command: define SBC.uart "UART2"

  - title: "Setup Programming Session"
    steps:
      - command: agentCfg PROGSBC %SBC.uart%
        with:
          - "%FIRMWARE%"

  - title: "Program RP2350B via JLink"
    steps:
      - command: uart %SBC.uart%
        send: |
          /opt/SEGGER/JLink/JLinkExe -device RP2350_M33_0 -if SWD -speed 4000 -autoconnect 1
          r
          h
          exec SetCompareMode = 0
          loadfile /run/pltagent/mnt/%FIRMWARE%
          r
          g
          q
        extract: "Program speed: (\\d+)"
        extractKey: JLINK_RETVAL
        timeout: 5s
      - command: eval "JLINK_RETVAL != ''"
        fail: "J-Link programming failed; check UART2 logs"
```

> **NOTE:** J-Link exits with 0 even when programming fails, so the plan extracts the Program speed line as the success signal instead of checking the exit code. exec SetCompareMode = 0 forces a re-flash rather than skipping unchanged sectors.

> **TIP:** J-Link interaction can be inspected in the UART2 logs in the Test Report.

**Program Bento Board with Flashr**

**Test Station**

| SKU | Model No. | Model Name |
|---|---|---|
| SKU-6 | PLT-106 | Production Line Tool |
| SKU-7 | PER-101 | Test Agent |
| SKU-28 | PER-401 | Flashr |
| SUB-67 | Bento Board | Device Under Test |

**Connection**

| Device A | Connector | Cable P/N | Connector | Device B |
|---|---|---|---|---|
| SKU-6 | USB-A (Port 1) | TBD | USB-C (PLT port) | SKU-7 |
| SKU-7 | USB-A (Port 2) | TBD | USB | SKU-28 |
| SKU-28 | 20-pin Header | TBD | J1 Tag-Connect | SUB-67 |
| SKU-6 | USB-A (Port 2) | TBD | USB-C | SUB-67 |

**YAML test plan**

Program the RP2350B with bento_blinky.hex, available from the v1.0.1 firmware release (https://github.com/bcdevices/bento-zephyr-fw/releases/tag/v1.0.1). Add bento_blinky.hex to the PLTcloud project alongside the test plan.

```yaml
title: "Bento Flashing Demo"
description: "Flash RP2350B via PER-101 Test Agent and Flashr"

suite:
  - title: "Defines"
    steps:
      - command: define FIRMWARE.filename "bento_blinky.hex"
      - command: define AGENT.vidpid "6666:8001"
      - command: define FIRMWARE.target "rp2350"
      - command: define DUT.vidpid "2fe3:0004"

  - title: "Setup Programming Session"
    steps:
      - command: usb detect
        id: "%AGENT.vidpid%"
        timeout: 30s
      - command: agentCfg PROGSBC UART2
        id: "%AGENT.vidpid%"
        retry: 3
        with:
          - "%FIRMWARE.filename%"
  - title: "Program RP2350B via Flashr"
    steps:
      - command: agentExec PROGSBC "flashr-flash %FIRMWARE.target% /run/pltagent/mnt/%FIRMWARE.filename%"
        timeout: 30s
```
