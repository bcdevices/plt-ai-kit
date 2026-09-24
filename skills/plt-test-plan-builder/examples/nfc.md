# NFC Examples

Snippets for detecting and writing an NFC tag.

## NFC Interaction

Source: `TestPlanReference/nfc/`

Examples using NFC to interact with the DUT.

**Detect**

Example: Detect NTAG and check UID.

```yaml
- ident: NFC-DETECT
  title: "Detect NTAG"
  steps:
  - command: nfc ntag-detect
    extractKey: NFC_UID
  - command: eval "NFC_UID == '5f4097d8de28ac'"
```

**Write**

Example: Program NDEF message with two text records.

```yaml
- ident: NFC-WRITE
  title: "Write NFC"
  steps:
  - command: define CODE 123
  - command: nfc write NTAG213 text:"Sample Text" text:%CODE%
```

**Commands**

- eval (`TestPlanReference/command/eval/`)
- nfc (`TestPlanReference/command/nfc/`)
