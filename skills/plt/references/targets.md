# Programming Targets

The `target` values accepted by `program`, `erase`, `identify`. A
column shows which commands accept each target; `identify` supports a
subset, since MCU identification needs vendor-specific register reads. Each
page's own notes on targets (CMSIS packs, USB-DFU, clock-frequency suffixes)
are with the command in `references/commands/programming.md`.

The list covers commonly used targets. Further MCU-specific targets are
supported by the underlying programmer; contact Blue Clover Devices if the
one you need is not listed.

## Target values

| Target | Description | program | erase | identify |
|---|---|---|---|---|
| `ATSAMD` | Microchip (Atmel) SAM D1x/D2x, C2x, L2x, R2x or R3x (SWD) | yes | yes |  |
| `ATSAMD_DAP` | Microchip (Atmel) SAM D1x/D2x, C2x, L2x, R2x or R3x (USB, DAPlink) | yes | yes |  |
| `ATSAME5` | Microchip (Atmel) SAM D5x/E5x (SWD) | yes | yes |  |
| `ATSAME5_DAP` | Microchip (Atmel) SAM D5x/E5x (USB, DAPlink) | yes | yes |  |
| `AVRATmega168P_ISP` | Microchip (Atmel) AVR ATmega168P(A) (JTAG:ISP) | yes | yes | yes |
| `AVRATmega168P_XPm` | Microchip (Atmel) AVR ATmega168P(A) (USB, XPmini) | yes | yes | yes |
| `AVRATmega168PB_ISP` | Microchip (Atmel) AVR ATmega168PB (JTAG:ISP) | yes | yes | yes |
| `AVRATmega168PB_XPm` | Microchip (Atmel) AVR ATmega168PB (USB, XPmini) | yes | yes | yes |
| `CC1352_DAP` | TI CC1352P1, CC1352R1 RFSoC (USB, CMSIS-DAP) | yes | yes | yes |
| `CC1352P7_DAP` | TI CC1352P7 RFSoC (USB, CMSIS-DAP) | yes | yes | yes |
| `CMSIS` | CMSIS-DAP programmer, requires pack: and target: fields (USB) | yes | yes |  |
| `EFM32` | Silicon Labs EFM32 MCU (SWD) | yes | yes |  |
| `EFR32` | Silicon Labs EFR32 RFSoC (SWD) | yes | yes |  |
| `ESP32_UART` | Espressif ESP32 RFSoC (UART) | yes | yes | yes |
| `LPC11xx` | NXP LPC11xx MCU (SWD) | yes | yes |  |
| `nRF52` | Nordic nRF52 RFSoC (SWD) | yes | yes | yes |
| `nRF52_DAP` | Nordic nRF52 RFSoC (USB, CMSIS-DAP) | yes | yes | yes |
| `nRF52_JLink` | Nordic nRF52 RFSoC (USB, JLink) | yes | yes | yes |
| `nRF91` | Nordic nRF9160 RFSoC:Cortex-M33 (SWD) | yes | yes | yes |
| `nRF91_JLink` | Nordic nRF9160 RFSoC:Cortex-M33 (USB, JLink) | yes | yes | yes |
| `PIC18F25K20` | Microchip PIC18F25K20 (JTAG:ICSP) | yes | yes |  |
| `PIC18F25K20_PK2` | Microchip PIC18F25K20 (USB, PICkit2) | yes | yes |  |
| `PN7360` | NXP PN7360 (SWD) | yes | yes |  |
| `PN7362` | NXP PN7362 (SWD) | yes | yes |  |
| `PN7412` | NXP PN7412 (SWD) | yes | yes |  |
| `PN7462` | NXP PN7462 (SWD) | yes | yes |  |
| `PSoC4` | Infineon (Cypress) PSoC4 (SWD) | yes | yes |  |
| `PSoC6` | Infineon (Cypress) PSoC6 (SWD) | yes | yes |  |
| `PSoC6_KP3` | Infineon (Cypress) PSoC6 (USB, KitProg3) | yes | yes |  |
| `RP2040` | Raspberry Pi RP2040 (SWD) | yes | yes |  |
| `RP2040_DAP` | Raspberry Pi RP2040 (USB, CMSIS-DAP) | yes | yes |  |
| `STM32F1` | ST STM32F1xx MCU (SWD) | yes | yes | yes |
| `STM32F1_STLink` | ST STM32F1xx MCU (USB, ST-Link) | yes | yes | yes |
| `STM32F2` | ST STM32F2xx MCU (SWD) | yes | yes | yes |
| `STM32F2_STLink` | ST STM32F2xx MCU (USB, ST-Link) | yes | yes | yes |
| `STM32F4` | ST STM32F4xx MCU (SWD) | yes | yes | yes |
| `STM32F4_STLink` | ST STM32F4xx MCU (USB, ST-Link) | yes | yes | yes |
| `STM32G0` | ST STM32G0xx MCU (SWD) | yes | yes | yes |
| `STM32G0_STLink` | ST STM32G0xx MCU (USB, ST-Link) | yes | yes | yes |
| `STM32G4` | ST STM32G4xx MCU (SWD) | yes | yes | yes |
| `STM32G4_STLink` | ST STM32G4xx MCU (USB, ST-Link) | yes | yes | yes |
| `STM32L0` | ST STM32L0xx MCU (SWD) | yes | yes | yes |
| `STM32L0_STLink` | ST STM32L0xx MCU (USB, ST-Link) | yes | yes | yes |
| `STM32L4` | ST STM32L4xx MCU (SWD) | yes | yes | yes |
| `STM32L4_STLink` | ST STM32L4xx MCU (USB, ST-Link) | yes | yes | yes |
| `STM32L5` | ST STM32L5xx MCU (SWD) | yes | yes | yes |
| `STM32L5_STLink` | ST STM32L5xx MCU (USB, ST-Link) | yes | yes | yes |
| `STM32H7` | ST STM32H7xx MCU (SWD) | yes | yes | yes |
| `STM32H7_DualBank` | ST STM32H7xx MCU, dual-bank flash (SWD) | yes | yes | yes |
| `STM32H7_STLink` | ST STM32H7xx MCU (USB, ST-Link) | yes | yes | yes |
| `MAX32690` | Analog Devices (Maxim) MAX32690 (SWD) |  |  | yes |
| `MAX32690_JLink` | Analog Devices (Maxim) MAX32690 (USB, JLink) |  |  | yes |
| `STM32F0` | ST STM32F0xx MCU (SWD) |  |  | yes |
| `STM32F0_STLink` | ST STM32F0xx MCU (USB, ST-Link) |  |  | yes |
| `STM32F3` | ST STM32F3xx MCU (SWD) |  |  | yes |
| `STM32F3_STLink` | ST STM32F3xx MCU (USB, ST-Link) |  |  | yes |
| `STM32L1_Cat12` | ST STM32L1xx Category 1 or 2 MCU (SWD) |  |  | yes |
| `STM32L1_Cat3` | ST STM32L1xx Category 3 MCU (SWD) |  |  | yes |
| `STM32L1_Cat456` | ST STM32L1xx Category 4, 5, or 6 MCU (SWD) |  |  | yes |
| `USB-DFU` | USB Device Firmware Upgrade (DFU 1.0, 1.1) (USB) | yes |  |  |

## Target documentation pages

- Analog Devices — `target/analog/`
- Analog Devices MAX32690 — `target/analog/max32690/`
- ESP32 — `target/esp/esp32/`
- Espressif Systems — `target/esp/`
- CMSIS — `target/generic/cmsis/`
- Generic — `target/generic/`
- SD-Card — `target/generic/sdcard/`
- USB Mass Storage device — `target/generic/usb-msd/`
- Program Targets — `target/`
- Infineon ACG1F — `target/infineon/acg1f/`
- Infineon CCG3PA — `target/infineon/ccg3pa/`
- Infineon Technologies — `target/infineon/`
- Infineon PSoC4 — `target/infineon/psoc4/`
- Infineon PSoC6 — `target/infineon/psoc6/`
- Microchip AVR ATmega168P/PA/PB — `target/mcp/atmega168pb/`
- Microchip SAMD Series — `target/mcp/atsamd/`
- Microchip SAM D5x/E5x — `target/mcp/atsamde5x/`
- Microchip SAM G5 Series — `target/mcp/atsamg5x/`
- PIC16 Intel HEX File LVP/HVP Checker — `target/mcp/hvp-checker/`
- Microchip Technology — `target/mcp/`
- Microchip PIC — `target/mcp/pic/`
- Microchip PIC18 — `target/mcp/pic18/`
- Melexis — `target/melexis/`
- Melexis MLX91804 — `target/melexis/mlx9180x/`
- Nordic Semiconductor — `target/nordic/`
- nRF52 — `target/nordic/nrf52/`
- nRF53 — `target/nordic/nrf53/`
- nRF54 — `target/nordic/nrf54/`
- nRF91 — `target/nordic/nrf91/`
- NXP Semiconductors — `target/nxp/`
- NXP LPC11xx — `target/nxp/lpc11xx/`
- NXP i.MX8 — `target/nxp/mimx8xx/`
- NXP i.MX RT1xxx — `target/nxp/mimxrt1xxx/`
- NXP i.MX RTxxx — `target/nxp/mimxrtxxx/`
- NXP PN736x/74x2 — `target/nxp/pn736x_74x2/`
- SiLabs EFM32/EFR32 — `target/silabs/efmr32/`
- Silicon Labs — `target/silabs/`
- STMicroelectronics — `target/st/`
- STM32F0 — `target/st/stm32f0/`
- STM32F1 — `target/st/stm32f1/`
- STM32F2 — `target/st/stm32f2/`
- STM32F3 — `target/st/stm32f3/`
- STM32F4 — `target/st/stm32f4/`
- STM32G0 — `target/st/stm32g0/`
- STM32G4 — `target/st/stm32g4/`
- STM32H7 — `target/st/stm32h7/`
- STM32L0 — `target/st/stm32l0/`
- STM32L1 — `target/st/stm32l1/`
- STM32L4 — `target/st/stm32l4/`
- STM32L5 — `target/st/stm32l5/`
- STM8 — `target/st/stm8/`
- TI CC13xx/CC26xx — `target/ti/cc13xx_26xx/`
- Texas Instruments — `target/ti/`
- XMOS — `target/xmos/`
- XMOS XCORE-200 — `target/xmos/xcore200/`
- XMOS XCORE.AI — `target/xmos/xcoreai/`
