# USB Examples

Snippets for identifying USB devices by VID:PID or path, USB-CDC and USB-MSC, and host and device roles.

## USB Interaction

Source: `TestPlanReference/usb/`

**USB Device Identification**

**USB Device ID (VID:PID)**

PLT-300A can use USB Vendor ID and USB Product ID to interact with USB devices.

Vendor IDs are controlled by the USB Implementers Forum (https://www.usb.org/about), while the Product ID is assigned by the device manufacturer.

Example ids:

- id: "0x2e8a:0x0003" Raspberry Pi Pico in UF2 bootloader.
- id: "0x046d:0xc080" Logitech Gaming Mouse G303.

**USB Device Paths**

PLT-300A uses USB Device Paths in cases where:

- Multiple devices of the same type are connected simultaneously.
- Port power control is needed.
- The VID:PID of the device is unknown or may change.

USB device paths are strings, a sequence of numbers separated by periods. The numbers are port numbers, and the sequence is the path to the target device.

| Port | Port Number | Location |
|---|---|---|
| DUT USB-C | 1 | Rear, left side of DUT area. |
| Accessory 1 | 2 | Rear, bottom-left of Accessories area. |
| Accessory 2 | 3 | Rear, top-left of Accessories area. |
| Accessory 3 | 4 | Rear, bottom-right of Accessories area. |
| Accessory 4 | 5 | Rear, top-right of Accessories area. |
| Front Left | 6 | Front, left connector. |
| Front Right | 7 | Front, right connector. |

Example paths:

- path: "1" Device connected to the DUT USB-C port.
- path: "2.1" Device on port 1 of a hub connected to the Accessory 1 port.
- path: "1.1.1" Device on port 1 of a hub connected to port 1 of a hub connected to the DUT USB-C port.

> **TIP:** At the start of test execution, the DUT USB-C port is powered off. To power on the port, use usb power on (`TestPlanReference/command/usb/`).

**Commands**

- usb detect (`TestPlanReference/command/usb_detect/`)
- usb power (`TestPlanReference/command/usb_power/`)
- usb reset (`TestPlanReference/command/usb_reset/`)

**USB-CDC**

**Commands**

- uartCfg (`TestPlanReference/command/uartCfg/`)

**USB-MSC**

**Commands**

- usb storage (`TestPlanReference/command/usb_storage/`)

**Examples**

- Example Projects (`samples/`) > Board-specific (`samples/board/`) > Raspberry Pi Pico (`samples/board/rpi_pico/`)
- Example Projects (`samples/`) > SBC-powered PPC (`samples/ppcsbc/`) > Nordic nRF Command Line Tools (`samples/ppcsbc/nordic-nrfjprog/`)
- Example Projects (`samples/`) > SBC-powered PPC (`samples/ppcsbc/`) > NXP Secure Provisioning SDK (`samples/ppcsbc/nxp-spsdk/`)

**USB Roles**

**Device Role**

The PLT-300A can be used to test a DUT in USB Device Role without any extra additions: the PLT-300A acts as the host, with the DUT connected to the Type-C port on the rear of the PLT-300A.

In case the Pogo-Pin Cassette (PPC) contains an additional SBC with which USB interaction from the PLT is required (for example, to update the SBC firmware over USB), the PPC can be equipped with a USB 2.0 or USB 3.0 hub.

**Host Role**

To test interaction with a DUT in USB Host Role, a USB Peripheral needs to be added to the test fixture, for example by including an USB Device-capable SBC like the Raspberry Pi Zero in the Pogo-Pin Cassette (PPC).

The DUT acts as the host, with the SBC USB Device port connected to the USB Host port of the DUT. The SBC can be controlled from the test plan with a UART connection between the SBC and the PLT.

In case USB interaction from the PLT is required (for example, to update the SBC's firmware over USB), the PPC should be equipped with a USB hub that allows switching between two different hosts, such as the Microchip USB5807C Hub Controller included in the PLT-300A Breakout Board.

**External References**

- Raspberry Pi Zero - Raspberry Pi (https://www.raspberrypi.com/products/raspberry-pi-zero/)
- usb5807c | Microchip Technology (https://www.microchip.com/en-us/product/USB5807C)
