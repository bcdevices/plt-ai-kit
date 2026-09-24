# Test Plan YAML and Keys

The test plan YAML definition (top-level keys, items, steps and their fields) and keys: defining, extracting and substituting `%KEY%` values. The authoritative field definitions are in the bundled JSON Schema, `references/test.plan-<version>.schema.json`.

## Test Plan YAML definition

Source: `TestPlanReference/yaml/`

In-circuit and Finished Goods (FG) test plans can be transcribed as PLT test plan (.YAML) files.

Example: A minimal test suite, with a single test item, scanning a bar code.

```yaml
title: "PLT demo: Scan"
suite:
- ident: SCAN-T1
  title: "Scan MAC address"
  steps:
  - command: scan ANY
```

**Test Plan Structure**

PLT test suites are encoded as YAML text files, starting with the test suite title.

```yaml
title: "PLT demo: Scan"
```

The title: is followed by the suite: section, containing the test items in the test plan.

**Test Items**

Test items are identified with an ident: line, can contain a descriptive title, and should contain one or more test item steps.

> **TIP:** The ident: field can be used to match PLT test plan items with items in the ICT and FG Test Plan .XLSX files or documents.

The ident: field can be omitted, in which case test items will be automatically enumerated. A top-level identPrefix: field can be used to set common prefix for auto-generated test item identifiers.

During test execution, all test item steps need to complete successfully for the test item to succeed.

**Test Item Steps**

Test item steps consist of command: blocks. A Test Item can contain multiple Test Item steps.

**Retries**

Retry counts can be set at the test item or at the test item step level, by adding a retry: field.

```yaml
title: "Retries"
identPrefix: "R"
suite:

- title: "Test Item retries"
  retry: 3
  steps:
  - command: sleepms 1000
  - command: operator Manual

- title: "Test Item retries"
  steps:
  - command: sleepms 1000
  - command: operator Manual
    retry: 3
```

**Command Reporting**

To improve the clarity of test execution feedback, command steps can include title: and fail: fields.

These fields allow test plan authors to provide human-readable descriptions and error guidance, which are displayed both during test execution and in the test reports. This helps operators understand the purpose of each step and what to do if something goes wrong.

The title: field can be used to provide a DUT-specific description of what the step is performing.

The fail: field defines a custom error message shown when the step fails. This message can provide guidance for troubleshooting or suggest corrective actions, such as checking solder joints or verifying power levels.

```yaml
title: "command with title and fail fields"
suite:

- steps:
   - command: measure voltageDATP01 >100mV
     title: "validating D1 connection"
     fail: "check for D1 solder defect"
```

**Timeouts**

Timeouts can be set at the test item or at the test item step level, by adding a timeout: field.

```yaml
title: "Basic timeout field usage"
suite:

- steps:
  - command: operator "Confirm"
    timeout: 5s
```

The timeout can be can be expressed in milliseconds, which is the default unit, or by using suffixes such as:

- "400ms" for 400 milliseconds.
- "5s" for a 5-second timeout.
- "1m" for a timeout of 1 minute.

**Conditional Execution**

Test items and individual test steps can be conditionally executed using the if: field.

This allows the test plan to include optional logic paths, perform validations only if certain conditions are met, or skip steps based on dynamic values.

if: expressions must evaluate to a boolean value (true or false) and can use variables defined earlier in the test plan (via the define (`TestPlanReference/command/define/`) command or the extractKey: field of a test step).

> **TIP:** Use conditional execution to control whether a test item or step is run, based on runtime conditions such as values returned from earlier steps, PPC properties, or external environment setup.

**Item-level Conditional Execution**

The if: field may be added to any test item to control whether the entire item (and all its steps) should be executed.

```yaml
title: "Conditional test item execution"
suite:
  - title: "Always runs"
    steps:
      - command: define A "1"
  - title: "Conditionally skipped"
    if: "false"
    steps:
      - command: operator "This will be skipped"
```

**Step-level Conditional Execution**

Individual steps can also be conditionally executed by including the if: field inside a step.

```yaml
title: "Conditional step execution"
suite:
  - title: "Define variable"
    steps:
      - command: define B "1"
  - title: "Mixed steps"
    steps:
      - command: eval "numeric(B) + 1"
        title: "This step is skipped"
        if: "false"
        extractKey: B
      - command: eval "numeric(B) + 1"
        extractKey: B
```

**Supported Expressions**

The if: condition can use the following elements:

- Literal values: true, false
- Variables previously defined or extracted: A, B, etc.
- Simple expressions: numeric(A) > 1, A == 'enabled'

> **NOTE:** Expressions are evaluated in the same context as eval (`TestPlanReference/command/eval/`) commands and must return a boolean result to be valid as an if: condition.

**Teardown Section**

The optional teardown: section defines cleanup steps after test execution, such as resetting equipment or powering down devices.

Teardown steps run after the test items finish, whether they passed, failed, or were aborted by the operator. Teardown stops at its first failing step, so put power-down steps first.

Example:

```yaml
title: "Simple Test Plan with Teardown"
suite:

- title: "Perform Test"
  steps:
  - command: pin RDTP01 output high
  - command: operator "Run test"

teardown:
  steps:
  - command: pin RDTP01 output low
```

**Calibration Section**

Some test setups may require additional calibration, which can be specified in the YAML test plan with an optional top-level calibration: section.

```
calibration:
- [ppc: <ppcID>]
  [impedance: <impedanceOffset>]
  [voltage: <voltageOffset>]
  [voltageDATP07: <voltageOffset>]
  [voltageDATP08: <voltageOffset>]
  [voltageDATP09: <voltageOffset>]
  [voltageDATP10: <voltageOffset>]
  [voltageDATP11: <voltageOffset>]
  [voltageDATP12: <voltageOffset>]
  [voltageMUX0: <voltageOffset>]
  [voltageMUX1: <voltageOffset>]
  [voltageMUX2: <voltageOffset>]
  [voltageMUX3: <voltageOffset>]
  [current: <currentOffset>]
  [current3V3: <currentOffset>]
  [current5V: <currentOffset>]
  [currentVARV: <currentOffset>]
- ...
```

The following fields can be set in a calibration entry:

| Field | Description |
|---|---|
| ppc: | Define the PPC for which this calibration entry should be applied. If omitted, the section defines the default offsets, to which a PPC-specific calibration section would be added. |
| impedance: | Specifies the offset for impedance measurements. |
| voltage: | Specifies the offset for voltage measurements. |
| voltageDATP07: | Specifies the offset for voltage measurements on the voltageDATP07 measurement channel. Overrides the offset specified in the voltage: field. |
| voltageDATP08: | Specifies the offset for voltage measurements on the voltageDATP08 measurement channel. Overrides the offset specified in the voltage: field. |
| voltageDATP09: | Specifies the offset for voltage measurements on the voltageDATP09 measurement channel. Overrides the offset specified in the voltage: field. |
| voltageDATP10: | Specifies the offset for voltage measurements on the voltageDATP10 measurement channel. Overrides the offset specified in the voltage: field. |
| voltageDATP11: | Specifies the offset for voltage measurements on the voltageDATP11 measurement channel. Overrides the offset specified in the voltage: field. |
| voltageDATP12: | Specifies the offset for voltage measurements on the voltageDATP12 measurement channel. Overrides the offset specified in the voltage: field. |
| voltageMUX0: | Specifies the offset for voltage measurements on the voltageDATP09 measurement channel. Overrides the offset specified in the voltage: field. |
| voltageMUX1: | Specifies the offset for voltage measurements on the voltageDATP10 measurement channel. Overrides the offset specified in the voltage: field. |
| voltageMUX2: | Specifies the offset for voltage measurements on the voltageDATP11 measurement channel. Overrides the offset specified in the voltage: field. |
| voltageMUX3: | Specifies the offset for voltage measurements of the voltageDATP12 measurement channel. Overrides the offset specified in the voltage: field. |
| current: | Specifies the offset for current measurements. |
| current3V3: | Specifies the offset for current measurements of the current3V3 measurement channel. Overrides the offset specified in the current: field. |
| current5V: | Specifies the offset for current measurements of the current5V measurement channel. Overrides the offset specified in the current: field. |
| currentVARV: | Specifies the offset for current measurements of the currentVARV measurement channel. Overrides the offset specified in the current: field. |

With the following argument values:

| Argument | Description |
|---|---|
| ppcID | PPC identifier for a ppc: field, to define a calibration specific to a particular PPC. |
| impedanceOffset | Offset for impedance measurements. Can be specified with nOhm, uOhm/µOhm, mOhm, Ohm, kOhm/KOhm or MOhm suffixes. If no suffix is specified, the offset is assumed to be specified in Ohm. |
| voltageOffset | Offset for voltage measurements. Can be specified with nV, uV/µV, mV, V, kV/KV or MV suffixes. If no suffix is specified, the offset is assumed to be specified in Volt. |
| currentOffset | Offset for current measurements. Can be specified with nA, uA/µA, mA or A suffixes. If no suffix is specified, the offset is assumed to be specified in Ampere. |

Example:

*Example test plan with a Calibration Section*

```yaml
title: "test plan with calibration"
identPrefix: "ICT-T"

calibration:
# Default offsets
- impedance: -100 # 100 Ohm
  voltage: +20mV # Default for all voltage channels
  voltageDATP01: +40mV
  voltageMUX2: +20mV
  voltageMUX3: +30mV
  currentVARV: -20mA
# Additional offsets specific to a particular PPC
- ppc: 39c8db  # Additional offsets for this PPC
  impedance: +120Ohm
  voltageDATP08: -10mV
  current5V: +100mA

suite:

- title: "Impedance Measurement"
  steps:
  - command: mux 0 RATP02
  - command: mux 1 RATP17
  - command: mux 2 RA
  - command: mux 3 RVREF
  - command: short 0 2 set
  - command: short 1 3 set
  - command: measure impedance 10-20Ohm
```

**runs-on section**

An optional runs-on: section allows specifying test execution constraints.

Example: test plan requiring pltOS v1.9

```yaml
runs-on:
  version: "1.9"

suite:
- steps:
  - command: operator "Hello"
```

Example: Complex constraints

```yaml
title: "Complex constraints"

runs-on:
  # Supported pltOS version(s)
  version:
  # Multiple version constraints can be provided (OR)
  - "1.2.3"
  - "~> 2.0"
  # Comma-separate constraints (AND)
  - ">= 5.0.0, < 7.2.3"

  # Only on PLTs with attached PPCs with any of these IDs
  ppc:
  - "a32fa1"
  - "323213"

  model:
  - "PLT-200A"
  - "PLT-300A"

suite:
  - ident: "ICT1"
    steps:
    - command: sleepms 1000
```

## Keys

Source: `TestPlanReference/keys/`

User Keys in PLT Test Plans are dynamic placeholders for storing and reusing values during test execution. These values can be set in the test plan, or extracted from command outputs.

**Set Key**

The define (`TestPlanReference/command/define/`) command can be used to assign assign a value to a key. These values are stored as strings and can be referenced in commands.

*PLT Test Plan: Define Keys*

```yaml
title: "Define Keys Example"
suite:
- ident: DEFINE-KEYS
  steps:
  # Define two keys with initial values
  - command: define RETVAL 5
  - command: define MSG "Hello!"
```

**Commands**

- define (`TestPlanReference/command/define/`)

**Extracting Keys**

Most commands support extracting the test value result in a key, by specifying name of the key as the value of an extractKey: field.

Example: Measurement

*PLT Test Plan: : Measure Voltage and Store in Key*

```yaml
title: "Measure Voltage and Store in Key"
suite:
- ident: MEASURE-EXTRACT
  steps:
  - command: measure voltageDMM DATP01 3.25-3.35V
    extractKey: VOLTAGE
```

In this case, the voltage measurement result is stored in the VOLTAGE key.

Example: UART Interaction

*PLT Test Plan: Capture UART Data in Key*

```yaml
title: "Capture UART Data in Key"
suite:
- ident: UART-EXTRACT
  steps:
  - command: uart UART0
    send: "AT+ICCID\r\n"
    expect: "+CCID:"
    extract: "CCID: (\\d{20})\r\n"
    extractKey: ICCID
```

In this example, the ICCID from the UART response is extracted and stored in the ICCID key.

**Commands**

- value (`TestPlanReference/command/value/`)
- measure (`TestPlanReference/command/measure/`)
- uart (`TestPlanReference/command/uart/`)

**Referencing Keys**

Once set, keys can be referenced in other commands by using %KEYNAME%. This substitutes the key’s value as a string before the command is executed.

Example: Using %KEYNAME% in Commands

*PLT Test Plan: Use Key in String Substitution*

```yaml
title: "Use Key in String Substitution"
suite:
- ident: USE-STRING-KEY
  steps:
  - command: define MSG "Hello!"
  - command: operator %MSG%
  - command: eval "%RETVAL% == '5'"
```

In this example:

- The %MSG% key is replaced by "Hello!" in the operator command.
- The eval (`TestPlanReference/command/eval/`) command substitutes %RETVAL% with "5" and performs a string comparison.

*PLT Test Plan: Keys as Signal Aliases*

```yaml
title: "Keys as Signal Aliases"
suite:
- ident: ICT-T0
  title: "Set variables"
  steps:
  - command: define probe.VBUS DATP01
- ident: ICT-T1
  title: "Measure VBUS"
  steps:
  - command: measure voltageDMM %probe.VBUS% 3.25-3.35V
```

All keys are included when making a webhook request.

*PLT Test Plan: Keys with Webhook*

```yaml
title: "Keys with Webhook"
suite:
- ident: ICT-T0
  title: "Set variables"
  steps:
  - command: define work_order 1011X02
- ident: ICT-T1
  title: "Invoke webhook with work_order key"
  steps:
  - command: webhook request
```

**Commands**

- define (`TestPlanReference/command/define/`)
- webhook (`TestPlanReference/command/webhook/`)

**Evaluating Keys**

The eval (`TestPlanReference/command/eval/`) command allows keys to be referenced directly as their underlying object. This means keys are accessed as numbers, strings, or measurements, depending on their content, without needing %.

*PLT Test Plan: Use Key in Numeric Evaluation*

```yaml
title: "Use Key in Numeric Evaluation"
suite:
- ident: USE-NUMERIC-KEY
  steps:
  - command: define RETVAL 5
  - command: eval "numeric(RETVAL) > 3"
```

In this example:

- The RETVAL key is set to the string "5", but inside the eval command, it is treated as a numeric value using the numeric() function.
- The eval command directly accesses the key without %, allowing the comparison as a number (5 > 3).

If %RETVAL% were used, it would expand the key as a string, which would be inappropriate for numeric comparisons.

Example: Using %KEYNAME% in eval for String Substitution

*PLT Test Plan: Use Key for String Substitution in Eval*

```yaml
title: "Use Key for String Substitution in Eval"
suite:
- ident: USE-STRING-EVAL
  steps:
  - command: define RETVAL 0
  - command: eval "%RETVAL% == '0'"
```

Here, %RETVAL% is substituted with the string "0", and the comparison is performed between two strings.

*PLT Test Plan: Evaluate Expressions*

```yaml
title: "Evaluate Expressions"
suite:
- title: "Eval"
  steps:
  - command: define test "AC1D"
  - command: eval "test != 'FOOBAR'"
  - command: eval "test == 'AC1D'"
  - command: define ONE 1
  - command: eval "numeric(ONE)+2"
    extractKey: SUM
  - command: eval "SUM == 3"
```

**Commands**

- eval (`TestPlanReference/command/eval/`)

**Evaluating Measurements**

Since measurement values stored in a key include the unit, the numeric(..) function can be used within expressions to cast the measurement result stored in a key, into a specific unit.

*PLT Test Plan: Evaluate Measurement*

```yaml
title: "Evaluate Measurement"
suite:
- title: "Evaluate Measurement"
  steps:
  - command: measure voltageDATP08 <4V
    extractKey: VOLTAGE
  - command: eval "(numeric(VOLTAGE, 'mV')) < 4000"
```

**Commands**

- eval (`TestPlanReference/command/eval/`)
- measure (`TestPlanReference/command/measure/`)
