# Operator interaction

## image

Set background image

```yaml
- command: image set <filename>

- command: image clear
```

| Argument | Description |
|---|---|
| `set` | Set background image |
| `clear` | Clear background image |
| `<filename>` | Filename of the PNG or JPEG file to show, relative to the test plan's suite folder |

The step fails if filename does not exist, or cannot be decoded as a PNG or JPEG image.

Examples: Operator Interaction (`TestPlanReference/operator/`)
## label

Set Label Substitutions

```yaml
- command: label keys <key> [<key>...]
```

The label command defines additional keys to substitute in the ZPL sent to the barcode printer, in addition to the default substitution keys.

Each key passed to label keys must have a value already stored for the DUT; its current value is substituted at label print time. define is one way to set such a key, but not the only one. extractKey on value or measure, for example, can also populate a key. A label keys step replaces the set of additional keys entirely; it does not add to keys registered by an earlier label keys step in the same plan.

Unlike eval and value, label does not expand %KEY% substitutions itself. It only registers which additional keys the label printer should look up when it builds the ZPL for the DUT.

| Key | Description |
|---|---|
| DUT_PRODUCT | Product name |
| DUT_VERSION | Version |
| DUT_SERIAL | DUT Serial number |
| MAC_ADDRESS | MAC address |
| BLEMAC | BLE MAC address |
| FAILURE_MSG | Test failure item (present only when printing a failure label) |

Examples: Label Printing (`TestPlanReference/barprint/`)
See also: `define`, `value`, `measure`
## operator

Operator Test

Instruct the operator to perform a manual test step, then present the operator with a Pass/Fail prompt on the PLT display. The step's result is determined entirely by the operator's response: choosing Pass passes the step, choosing Fail fails it.

```yaml
- command: operator <message>
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<message>` | Message to show on the PLT display, instructing the operator what to check or do |
| `<retryCount>` | Number of times to retry the test step (optional); this is the generic retry: step field, not specific to operator |

If the operator does not respond within the timeout (30 seconds by default; override with a timeout: step field), the step fails.

Examples: Operator Interaction (`TestPlanReference/operator/`)
## scan

Scan Barcode

Scan a barcode using USB-attached barcode scanner.

```yaml
- command: scan [<format>]
  [expect: [hex] <expectText>]
  [extract: <extractText>]
  [extractKey: <key>...]
  [retry: <retryCount>]
  [timeout: <timeout>]
  [with:
    [- trigger:<DDTPxx|RDTPxx> <kind> <level> [<triggerDuration>]]
```

| Argument | Description |
|---|---|
| `<format>` | Format of code to scan (optional as of pltOS v2.0.30) |
| `<expectText>` | Text to expect in the barcode. If the hex keyword is used, expectText is interpreted as a hex string. |
| `<extractText>` | Regular expression to extract (uses RE2 Syntax, except \C) |
| `<key>` | Key(s) in which to store extracted text. To save multiple values, use multiple capture groups. |
| `<retryCount>` | Number of times to retry the test step (optional) |
| `<timeout>` | Timeout, with time suffix ("500ms") or in milliseconds (default: 30s) |
| `<RDTPxx/DDTPxx>` | Optional trigger pin to initiate scanning. Only RDTP and DDTP probes are supported as trigger signals. |
| `<kind>` | Trigger kind: active (assert the level before scanning, release afterward), pulse (assert the level for triggerDuration, then release, before scanning starts), or none (no signal is driven). |
| `<level>` | Trigger level: high or low. Required for pulse; optional for active (defaults to low if omitted); not used for none. |
| `<triggerDuration>` | Pulse duration, e.g. 100ms or a plain integer number of milliseconds (pulse only; default: 100ms). |

At most one trigger: entry may be given under with:.

```yaml
title: "Scan serial number"
suite:
- steps:
  - command: scan ANY
    extractKey: MY_BARCODE
  - command: serial set %MY_BARCODE%
```

```yaml
title: "Scan barcode with expected substring"
suite:
- steps:
  - command: scan
    # "MN-004137-01EN"
    expect: "MN-"
    extractKey: BARCODE_EXPECTED
```

```yaml
title: "Scan barcode and extract multiple values"
suite:
- steps:
  - command: scan
    # "MN-004137-01EN"
    extract: "^MN-(\\d+)-(\\d+.*)$"
    extractKey: NUM SUFFIX
```

_Supported format values:_

| format | Description |
|---|---|
| ANY | Any barcode payload; the result is the raw scanned text. |
| MAC_ADDRESS | Requires the scanned payload to be a 48-bit MAC address in XX:XX:XX:XX:XX:XX form (17 characters, hex octets separated by colons); fails otherwise. On success, also records the value as the DUT's BLE MAC address in the report. |
| (omitted) | No format check. The raw payload is matched against expect (if given) and/or parsed with extract (if given). |

See also: Barcode Scanning (`TestPlanReference/barscan/`), Peripherals (`peripheral/`), Barcode Scanners (`peripheral/barscan/`)
