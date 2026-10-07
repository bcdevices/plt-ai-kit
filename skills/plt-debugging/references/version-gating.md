# Version Gating

Features that require a specific pltOS, agentOS or flashOS version (**New**, from
`.. versionadded::` annotations in the documentation), and bugs fixed in a
specific release (**Fixed**, from the release notes). If a step fails on a
plan that works elsewhere, compare the PLT's version against this table: a
feature newer than the PLT's version is missing, and a failure matching a
**Fixed** row is resolved by updating.

This table is current as of this skill's version. Releases published since
are listed at https://docs.pltcloud.com/releases/ — check there before concluding a
failure is not a known, fixed issue.

| Feature or fix | Kind | Version | Documentation |
|---|---|---|---|
| ZPL Template Filenames (Label Printing) | New | pltOS 2.0.32 | `TestPlanReference/barprint/` |
| agentCfg | New | pltOS 2.0 | `TestPlanReference/command/agentCfg/` |
| agentExec | New | pltOS 2.0.42 | `TestPlanReference/command/agentExec/` |
| canCfg | New | pltOS 2.0 | `TestPlanReference/command/canCfg/` |
| resume | New | pltOS 1.10.10 | `TestPlanReference/command/resume/` |
| scpi | New | pltOS 2.0 | `TestPlanReference/command/scpi/` |
| store | New | pltOS 2.3.27 | `TestPlanReference/command/store/` |
| uartBreak | New | pltOS 2.3.21 | `TestPlanReference/command/uartBreak/` |
| value | New | pltOS 2.0.30 | `TestPlanReference/command/value/` |
| wait | New | pltOS 1.10.3 | `TestPlanReference/command/wait/` |
| Conditional Execution (Test Plan YAML definition) | New | pltOS 2.2 | `TestPlanReference/yaml/` |
| flashr-flash - Program a target through Flashr | New | agentOS 1.6.2 | `agentOS/flashr-flash/` |
| flashr-update - Update Flashr firmware | New | agentOS 2.0.2 | `agentOS/flashr-update/` |
| USB network interface (agentOS) | New | agentOS 2.0.2 | `agentOS/` |
| Store-and-Forward (Edit Settings) | New | pltOS 2.3 | `pltcloud/webconsole/project/settings/basic/` |
| PLTOS-475: Avoid stale UART FDs. Fix to avoid lingering stale open file descriptors for the UART devices for every test plan run. | Fixed | pltOS 3.0.7 | `releases/pltOS/3.0/` |
| PLTOS-463: Fix in-app Power Off; boot with display on | Fixed | pltOS 3.0.6 | `releases/pltOS/3.0/` |
| PLTOS-474: Fixed UART port detection when multiple USB-CDC devices were connected to the PLT-106 | Fixed | pltOS 3.0.5 | `releases/pltOS/3.0/` |
| TGT-71: Fix openocd script error programming STM32L0 targets | Fixed | pltOS 2.4.13 | `releases/pltOS/2.4/` |
| PLTOS-437: Interactive UI dialogs fail early Fixes regression introduced in pltos-2.2.6 | Fixed | pltOS 2.3.10 | `releases/pltOS/2.3/` |
| PLTOS-437: Interactive UI dialogs fail early Fixes regression introduced in pltos-2.2.6 | Fixed | pltOS 2.2.10 | `releases/pltOS/2.2/` |
| PLTOS-419: last result: Serial line cut off. Fix layout regression introduced in pltOS v2.0.41 related to initial support for Asian fonts. | Fixed | pltOS 2.1.21 | `releases/pltOS/2.1/` |
| PLTOS-412: uartCfg: fix handling of previously opened UART channels | Fixed | pltOS 2.1.20 | `releases/pltOS/2.1/` |
| PLTOS-417: uart command: Fix regression introduced in pltOS v2.1.14 where the controller could consider the command was done before it really was | Fixed | pltOS 2.1.18 | `releases/pltOS/2.1/` |
| PLTOS-416: scan command: fix erroneous 'more extractKeys than results' failures | Fixed | pltOS 2.1.17 | `releases/pltOS/2.1/` |
| PLTOS-409: Fix deadlock on closing UART ports at end of test run | Fixed | pltOS 2.1.7 | `releases/pltOS/2.1/` |
| PLTOS-401: Fix test steps failing with exec: Wait was already called, instead of the actual failure message. | Fixed | pltOS 2.0.48 | `releases/pltOS/2.0/` |
| PLTOS-382: uart command: expect/extract flush race condition fix | Fixed | pltOS 2.0.38 | `releases/pltOS/2.0/` |
| PLTOS-367: Fix potential race condition when using a uart command with an expect: field. | Fixed | pltOS 2.0.33 | `releases/pltOS/2.0/` |
| PLTOS-336: PLT-300A internal firmware update stability fixes | Fixed | pltOS 2.0.32 | `releases/pltOS/2.0/` |
| PLTOS-366: Fix potential lock-up after internal firmware update failures | Fixed | pltOS 2.0.30 | `releases/pltOS/2.0/` |
| PLTOS-286: joulescope: fix handling of negative and partial bounds | Fixed | pltOS 2.0.29 | `releases/pltOS/2.0/` |
| PLTOS-345: PLTcloud client stability fixes, fixing some cases where PLT would need to be re-enrolled after an update | Fixed | pltOS 2.0.19 | `releases/pltOS/2.0/` |
| PLTOS-346: canCfg path: handling and CAN-FD dongle detection bug fixes. | Fixed | pltOS 2.0.17 | `releases/pltOS/2.0/` |
| PLTOS-347: Fix usb invalid subcommand error | Fixed | pltOS 2.0.16 | `releases/pltOS/2.0/` |
| PLTOS-344: Button handling stability fixes | Fixed | pltOS 2.0.15 | `releases/pltOS/2.0/` |
| PLTOS-341: Fix for internal PLT-300A firmware not being updated on some units. | Fixed | pltOS 1.11.10 | `releases/pltOS/1.11/` |
| PLTOS-334: UART stability fixes | Fixed | pltOS 1.11.8 | `releases/pltOS/1.11/` |
| PLTOS-324: Fix handling of test items without declared test steps | Fixed | pltOS 1.11.7 | `releases/pltOS/1.11/` |
| TGT-128: Fix MiniProg4 selection by id and path. | Fixed | pltOS 1.11.3 | `releases/pltOS/1.11/` |
| PLTOS-321: Fix user key substitution in uart command. | Fixed | pltOS 1.11.3 | `releases/pltOS/1.11/` |
| PLTOS-297: Fix the detail desult value of the resume command | Fixed | pltOS 1.10.11 | `releases/pltOS/1.10/` |
| PLTOS-298: Fix for an issue in factory reset handling | Fixed | pltOS 1.10.11 | `releases/pltOS/1.10/` |
| LY11-614: Fix RDTP Reset on PPCs without a RDTP00…RDTP15 I/O expander | Fixed | pltOS 1.10.10 | `releases/pltOS/1.10/` |
| PLTOS-284: Fix BLE adapter detection and connection retry issues. | Fixed | pltOS 1.10.9 | `releases/pltOS/1.10/` |
| TGT-113: fix STM32H7_DualBank targets | Fixed | pltOS 1.10.6 | `releases/pltOS/1.10/` |
| PLTOS-237: image command: fix path error | Fixed | pltOS 1.10.1 | `releases/pltOS/1.10/` |
| PLTOS-239: Fix nil dereference upon uartcmd errors | Fixed | pltOS 1.10.1 | `releases/pltOS/1.10/` |
| PLTOS-214: Fix uart send param propagation | Fixed | pltOS 1.9.15 | `releases/pltOS/1.9/` |
| PLTOS-198: Fix an "Error Retrieving Update" in some cases where no update was available. | Fixed | pltOS 1.9.13 | `releases/pltOS/1.9/` |
| PLTOS-187: Fixed "Unknown UART" issue introduced in pltOS v1.9.10. | Fixed | pltOS 1.9.11 | `releases/pltOS/1.9/` |
| PLTOS-129: Fix Cypress programming | Fixed | pltOS 1.8.14 | `releases/pltOS/1.8/` |
| PLTOS-82: Fix nRF9160 programming | Fixed | pltOS 1.8.8 | `releases/pltOS/1.8/` |
| PLTOS-92: Fix PLT-200A debug reset | Fixed | pltOS 1.8.8 | `releases/pltOS/1.8/` |
| Fix Standby Exit with single button press | Fixed | pltOS 1.8.4 | `releases/pltOS/1.8/` |
| Pulse power LED properly, fix standby timeouts after initial timeout. | Fixed | pltOS 1.8.4 | `releases/pltOS/1.8/` |
| PLTOS-80: Backport UART Observer Fix | Fixed | pltOS 1.7.56 | `releases/pltOS/1.7/` |
| PLTOS-29: Fix factory reset hang from PLTcloud | Fixed | pltOS 1.7.54 | `releases/pltOS/1.7/` |
| LY11-525: Fix enrollment check interval | Fixed | pltOS 1.7.54 | `releases/pltOS/1.7/` |
| Fix the GitHub Actions release build | Fixed | flashOS 0.6.1 | `releases/flashOS/0.6/` |
| Fix sstate caching | Fixed | agentOS 2.0.0 | `releases/agentOS/2.0/` |
| Fix USB MSC issues in AOS-6 Make the msc-host-handler more resilient during test plans executed on the PLT. Remove lines in the script that caused the USB port on the test agent to re-enumerate, which can cause the UART terminal on /dev/ttyGS0 to drop out. This appears to have led to failing test plans when the PLT occasionally failed to send follow up commands to the agent. | Fixed | agentOS 1.6.1 | `releases/agentOS/1.6/` |
