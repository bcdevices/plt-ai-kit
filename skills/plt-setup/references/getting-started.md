# PLT Getting Started

The published Getting Started guide and the PLT-106 setup and wiring reference. This is the source of truth for the order of the steps.

## Getting Started

Source: `getting-started/`

This guide takes you from unboxing your new PLT-106 (`plt-106/`) to your first test run. Each step links to the detailed page for more information.

The example programs a Bento Board (`samples/board/bento/`) through a Test Agent (`peripheral/ta/per-101/`) and a Flashr (`peripheral/prog/per-401/`). Neither the DUT nor the programmer are required: see Other targets and programmers.

> **TIP:** If you use a coding agent, consider installing the PLT AI Kit (`ai-kit/`) first. The agent can then guide you through the rest of these steps and write your test plans.

**Set up the hardware**

1. Assemble the PLT-106, connect its USB-C power input to a power supply, and connect its Ethernet port to a router or switch with DHCP and outbound Internet access.
2. Connect the rest of the station as shown in Common Wiring. Power the Test Agent externally, not from the PLT's USB port.
3. Power on the PLT.

Details: PLT-106 Setup and PLT Connectivity (`pltcloud/plt-connectivity/`).

**Create a PLTcloud account**

Sign up at https://pltcloud.com and create an organization. If you are joining an existing organization, use the email address your administrator invited.

Details: Create a PLTcloud Account (`pltcloud/webconsole/create/`).

**Enroll the PLT**

1. On the PLT, select Menu → Enroll. The PLT shows an enrollment code.
2. In the PLTs section of PLTcloud, select the Enroll PLT form and enter that code as the Activation code.

Details: Adding a PLT (`pltcloud/webconsole/plt/add/`).

**Create a project and deployment group**

A project holds your files and releases. A deployment group is a set of PLTs that run the same release.

1. Create a project (`pltcloud/webconsole/project/create/`).
2. Create a deployment group and assign your PLT to it.

**Create your first release**

A release combines a test plan with the files it needs. For the Bento Board:

1. Download bento_blinky.hex (https://github.com/bcdevices/bento-zephyr-fw/releases/download/v1.0.2/bento_blinky.hex) from the v1.0.2 firmware release (https://github.com/bcdevices/bento-zephyr-fw/releases/tag/v1.0.2).
2. Download the test plan, bento-flashr-blinky.yaml (https://github.com/bcdevices/test-plans/blob/main/bento/bento-flashr-blinky.yaml). It waits for the Test Agent, sends it the firmware, and programs the board:

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

3. Create a release containing both files.

To write your own plan, start with the Test Plan Reference (`TestPlanReference/`).

**Other targets and programmers**

The Bento Board and Flashr are only one option. You can program and test other hardware with other tools:

- Program Targets (`target/`) lists supported targets.
- Programmers (`peripheral/prog/`) lists supported programmers.
- SBC-powered PPC (`samples/ppcsbc/`) shows Test Agent programming tools, such as nrfutil and SEGGER J-Link Commander.
- Example Projects (`samples/`) has complete example projects.

**Run the test plan**

1. Deploy the release to your deployment group.
2. On the PLT, select Menu → Check for Updates → Update.
3. Run the test plan. The board is programmed and starts blinking.
4. View the test report in PLTcloud. See Manage Reports (`pltcloud/webconsole/report/`).

**Next steps**

You can improve your interactions with the PLT hardware and PLT Cloud with:

- Coding agent support: PLT AI Kit (`ai-kit/`) helps agents write and debug test plans, and Chat to Chip Firmware Flashing (`chattochip/`) shows the full path from a conversation to programmed firmware.
- Command line tool: pltutil CLI (`pltutil/`) uploads and deploys releases and waits for test reports from a terminal.
- Continuous integration support: Continuous Integration (`pltcloud/continuous-integration/`) uploads releases from a pipeline, and PLT Hardware CI (`pltcloud/hardware-ci/`) runs firmware on target hardware from GitHub.
- Slack integration: PLTcloud Slack App (`slack/`) shares test report notifications with your team.

## PLT-106 Reference

Source: `plt-106/`

**Setup**

1. Assemble the PLT-106.
2. Connect the USB-C power input to a power supply.
3. Connect the Ethernet port to a router or switch. The PLT uses this connection to reach PLTcloud, so the network must provide DHCP and outbound Internet access. See Network Requirements.
4. Press the power button on the front panel.

Next, enroll the PLT (`pltcloud/webconsole/plt/add/`) in PLTcloud. For the complete path to a first test run, see Getting Started (`getting-started/`).

**Connecting Devices**

The USB-A ports connect the PLT to the rest of your test station. This might include:

- A Test Agent (`peripheral/ta/per-101/`), which runs programming tools and scripts for the test plan.
- A DUT with a USB interface, which test plans reach with the USB commands (`TestPlanReference/usb/`).

**Common Wiring**

This station most commonly programs and tests a DUT through a Test Agent and a Flashr (`peripheral/prog/per-401/`). The Bento Board (`samples/board/bento/`) is the example DUT.

| From | To | Purpose |
|---|---|---|
| PLT-106 USB-A port 1 | Test Agent USB-C (PLT port) | Console, RAMDISK, network |
| Test Agent USB-A port 2 | Flashr USB | CMSIS-DAP probe |
| Flashr 20-pin header | Bento J1 Tag-Connect | SWD |
| PLT-106 USB-A port 2 | Bento USB-C | DUT USB and power |
| PLT-106 Ethernet | Network with DHCP and outbound Internet access | PLTcloud |

> **NOTE:** Power the Test Agent externally, not from the PLT's USB port.
