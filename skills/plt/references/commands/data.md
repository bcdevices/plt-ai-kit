# Keys and data capture

## define

Define user key

Manually defines a test plan key, which will be embedded in the test report and serial number requests performed as part of the current test plan.

```yaml
- command: define <key> <value>
```

| Argument | Description |
|---|---|
| `<key>` | Name of the test plan key. |
| `<value>` | Value for the key; can be any kind of string value. Any %KEY% substitutions in value (referencing an earlier define or a system key) are expanded immediately, before the value is stored. |

A key set with define is available to later eval expressions (by bare name) and to label (when named in a label keys step), and can override a system key of the same name (PRODUCT, VERSION, BOM_REV, DUT_ID, SERIAL_NUMBER, and others). A second define for the same key replaces its previous value.

Examples: Keys (`TestPlanReference/keys/`)
## store

Store file to Report Connector

Submit a file (through Store-and-Forward) to the S3 buckets defined in the Report Connector.

<key> is a user-defined key holding a file reference previously captured with extractKey:, such as the result of usb storage read. store looks up the key, resolves it to the in-memory file it references, and uploads that file's contents to the Report Connector, associated with the current DUT report.

```yaml
- command: store <key>
```

| Argument | Description |
|---|---|
| `<key>` | User key holding a file reference captured via extractKey: on an earlier step. |

> **NOTE:** The step fails if key is not set, or if it does not hold a valid file reference.

> **NOTE:** Earlier versions called the positional argument <memHandle>. The name changed to <key> to reflect that it is an ordinary user key (populated by an earlier step's extractKey:), not a distinct handle type. The command syntax and behavior are unchanged — existing test plans that pass a file-reference key continue to work.

See also: `agentCfg`, `usb storage`
