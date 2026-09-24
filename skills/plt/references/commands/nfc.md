# NFC

## nfc

NFC Interaction

Interact with DUT using NFC. Requires a supported NFC interface adapter device.

### `nfc ntag-detect`

Checks if an NFC NTAG is present at the adapter and reads its UID. Fails if no tag is detected.

```yaml
- command: nfc ntag-detect
  [extractKey: <uid>]
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<uid>` | The NTAG UID value can be extracted as a User Key (optional) |
| `<retryCount>` | Number of times to retry the test step (optional) |

Use nfc ntag-detect to confirm tag presence (and capture its UID) before or after an nfc write step. For example, this can be used to verify a tag was placed on the fixture, or to read back a UID for the report.

### `nfc write`

Encode one or more NDEF records and write the resulting NDEF message to the tag presented at the NFC adapter.

```yaml
- command: nfc write <TAGTYPE> <payload>...
  [retry: <retryCount>]
```

| Argument | Description |
|---|---|
| `<tagtype>` | Tag type (NTAG203, NTAG213 or NTAG216). Required argument; writing auto-detects the presented NDEF tag rather than branching on this value. |
| `<payload>` | One or more NDEF records to write. Currently only text:<string> (an NDEF Text record, language en) is supported. Other prefixes are rejected. |
| `<retryCount>` | Number of times to retry the test step (optional) |

Each payload argument becomes one NDEF record in the message written to the tag, in the order given.

Examples: NFC Interaction (`TestPlanReference/nfc/`)
