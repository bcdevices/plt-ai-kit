# Electrical Safety

The electrical safety checks to run before a plan applies power, so a short circuit or out-of-range voltage does not damage the PLT or the DUT.

## Electrical Safety

Source: `TestPlanReference/electrical-safety/`

Safety First

Best practices for safe and effective testing with the PLT.

**Human Safety**

Most importantly, consider the safety of test operators.

- If your tests require high-voltage or high-current, your fixture should be designed to prevent accidental contact with these hazards.

   - Fixtures should be enclosed in a case or with shielding to prevent accidental contact with high-voltage or high-current.

- If your tests include operator command steps, make sure that fixture power is off when the operator is expected to interact with the fixture.
- Incorporate checks in your tests to make sure that the fixture is "closed" before applying power to the device under test (DUT).

**Fixture Close Detect**

In the following code snippet, we check that the fixture is closed before applying power, to avoid exposed power rails. We're assuming that the fixture is designed such that the DDTP00 signal is connected to DUT_GND1 when the fixture is closed.

```yaml
- ident: FixtureClosed
  title: "Check that fixture is closed."
  steps:
  - command: measure continuity DDTP00 true
    ground: GND1
```

**PLT and Device Safety**

Care must be taken in designing a test plan to ensure that the PLT and the device under test (DUT) are not damaged during testing. Connecting the PLT to a DUT with a short circuit, or with a voltage or current that exceeds the PLT's specifications, can damage the PLT and/or the DUT.

**Power Safety**

Delivering power to your device under test (DUT) is a critical part of testing, and a common source of problems.

- When using the PLT's built-in power supply to power a device under test (DUT), make sure that the DUT's power requirements are within the PLT's specifications.

   - The PLT's power supply is rated for 1.8V, 3.3V, 5V, or variable 1.5~24V (up to 2A each). If your DUT requires more than 2A, you will need to use an external power supply.
   - External power sources can be controlled by the PLT using a relay or other external control mechanism.
   - In measuring your DUT's current requirements, you will need to consider inrush current in addition to steady-state current. For long-term reliability, the inrush current should be less than the PLT's rated current.
   - An external power supply may be needed to provide the necessary reliability margin for inrush current.

- DUT defects can be dangerous to the operator, the PLT, and the DUT itself. The most dangerous defects are input power rail short circuits.
- Use the PLT's electrical measurement capabilities to verify that the DUT does not have a short circuit or other electrical fault.

The best method to use in testing your DUT for power rail short circuits varies, depending on your device's design, and the other components in your test setup. The following are some techniques to use to check your DUT before applying power. In these examples we're assuming that the DUT has a single power input (DUT_PWR) and a single ground (DUT_GND1).

**Continuity Measurement**

Measure continuity between DUT_PWR and DUT_GND1 to verify that the DUT's power and ground pins are not shorted. This is the simplest method, but with other devices (programming interfaces, etc.) connected to the DUT, it may not be sufficient.

This test plan snippet shows how to measure continuity between DUT_PWR and DUT_GND1:

```yaml
- ident: PowerInputContinuity
  title: "Use continuity to check for short circuit between power and ground"
  steps:
  - command: measure continuity DATP00 false
    ground: GND1
```

**Resistance Measurement**

Measure resistance between DUT_PWR and DUT_GND1 to verify that there is sufficiently high resistance between power and ground. A low resistance indicates a short circuit. This method is more sensitive than measuring continuity, but again it may not be viable depending on your device's design or other components in your test setup.

You'll need to measure sample devices to set a threshold for what resistance is acceptable. In the example below, we found that the typical resistance between power and ground on our DUT was 3kOhm, so we set a minimum of 2kOhm.

```yaml
- ident: PowerInputResistance
  title: "Use resistance to check for short circuit between power and ground"
  steps:
  - command: measure resistance DATP00 >2kOhm
    ground: GND1
```

**Voltage Measurement**

Measure voltage between DUT_PWR and DUT_GND1. This method is useful in the case that other devices in your test setup are injecting power into the DUT (which makes measuring resistance or continuity difficult).

You'll need to measure typical floating voltage on your DUT to set a threshold for what voltage is acceptable. In the example below, we found that the typical floating voltage on our DUT was 1.0V, so we set a minimum of 0.5V.

```yaml
- ident: PowerInputVoltage
  title: "Use voltage to check for short circuit between power and ground"
  steps:
  - command: measure voltageDMM DATP00 >0.5V
    ground: GND1
```

**Signal Measurement Safety**

Once you've applied power to your DUT, you'll need to measure signals to verify that your DUT is functioning correctly. When measuring signals, you'll need to consider the voltage and current that the PLT can safely measure.

Keep the following in mind when designing your test plan:

- The majority of PLT signals are limited to a maximum of 5V (absolute maximum of 5.5V).
- Measurements above 5V can be made using the PLT-300's built-in digital multimeter (DMM) or an external DMM.
- The following signals can be used with the built-in DMM, up to 100V: DATP00…DATP06 and DDTP00…DDTP08.
- The DATP00…DATP06 and DDTP00…DDTP08 signals are safe to connect to voltages >5V by default, but it is possible to connect them to the PLT-300 mux sub-system, which is limited to 5V. Use caution when connecting these signals to the mux sub-system.

**Putting it Together**

The following is an example test plan that incorporates the best practices for safe and effective testing with the PLT.

```yaml
title: "High-Voltage DUT Test Plan Example"
suite:

- ident: SETUP
  title: "Setup the test environment"
  steps:
  # High voltage power connection is controlled by a relay wired to RDTP00.
  - command: define HighVoltageRelay "RDTP00"
  - command: define DUT_PWR "DATP00"
  - command: define FixtureClosed "DDTP00"
  - command: define 12VRail "DATP01"
  - command: define 5VRail "DATP02"
  - command: define 3V3Rail "DATP03"
  - command: define nRF52Firmware "high_voltage_control-v1.2.3.hex"

- ident: BARCODE
  title: "Scan DUT barcode."
  steps:
  - command: scan ANY
    extractKey: DUT_BARCODE
  - command: serial set %DUT_BARCODE%

- ident: InsertAndClose
  title: "Insert DUT into fixture and close."
  retry: 3  # Retry up to 3 times if the fixture is not closed.
  steps:
  - command: operator "Please insert DUT into fixture and close securely."
    timeout: 2m
  - command: measure continuity %FixtureClosed% true
    title: "Check if the fixture is closed"
    ground: GND1

- ident: Power.DetectShort
  title: "Check for short circuit between power and ground"
  steps:
  # We expect the resistance between DUT_PWR and GND1 to be >2kOhm,
  # anything less indicates a possible short circuit.
  - command: measure resistance %DUT_PWR% >2kOhm
    ground: GND1

- ident: Power.ApplyAndCheckRails
  title: "Apply power to DUT, check power rails."
  steps:
  # Double-check that the fixture is closed before proceeding.
  - command: measure continuity DDTP00 true
    ground: GND1
  # Activate HighVoltageRelay to apply power to DUT.
  - command: pin %HighVoltageRelay% output high
  - command: sleepms 250 "Allow time for power to stabilize."
  - command: measure voltageDMM %12VRail% 11.8-12.2V
    ident: "12VRail"
    ground: GND1
  - command: measure voltageDMM %5VRail% 4.9-5.1V
    ident: "5VRail"
    ground: GND1
  - command: measure voltageDMM %3V3Rail% 3.2-3.4V
    ident: "3V3Rail"
    ground: GND1

- ident: Program
  title: "Program DUT with firmware."
  steps:
  - command: identify nRF52
    ident: "Identify"
  - command: program nRF52 %nRF52Firmware%
    ident: "Program"

teardown:
  steps:
  - command: pin %HighVoltageRelay% output low
```
