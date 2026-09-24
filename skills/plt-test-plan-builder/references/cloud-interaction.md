# Cloud Interaction

Getting a serial number into a plan, either allocated by PLTcloud (monotonic counter or a webhook to your server) or set directly, e.g. from a scanned barcode, so it can be programmed into the DUT and printed on the label. For the webhook endpoint itself, see the `plt-cloud` skill.

## Cloud Interaction

Source: `TestPlanReference/cloud/`

Under Project Settings in PLTcloud, serial number allocation can be configured to use either monotonic counters, or through a webhook.

When using serial request, and a webhook is selected in PLTcloud, a JSON request will be sent containing:

```json
{
    "dut_id": "<DUT IDENTIFIER>",
    "serial_number": "<SERIAL NUMBER>",
    "ble_mac": "<BLE MAC>",
    "mcu_id": "<MCU ID>",
    "MYCUSTOMKEY": "my custom value"
}
```

The API endpoint should return something like:

```json
{
    "serial_number": "<SERIAL NUMBER>",
    "extra": {
       "name": "Ben"
    }
}
```

To extract the name field, use the serial request command as below:

```yaml
title: "Eventbrite"
suite:

- ident: SCAN
  title: "Scan"
  steps:
  - command: scan ANY
    extractKey: BARCODE

- ident: WEBHOOK
  title: "Lookup barcode"
  steps:
  - command: serial request NAME:name
  - command: operator %NAME%

- ident: PRINT
  title: "Print badge"
  steps:
  - command: label keys NAME
```

Using serial set, the serial number can be set directly from the test plan, for example using a key extracted from a barcode scan:

```yaml
title: "Scan serial number"
suite:
- steps:
  - command: scan ANY
    extractKey: BARCODE
  - command: serial set %BARCODE%
```

**Commands**

- serial (`TestPlanReference/command/serial/`)
- webhook (`TestPlanReference/command/webhook/`)
