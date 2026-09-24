# Design for Test

What to test and design for manufacturing. Board design, firmware design and PPC (Pogo-Pin Cassette) guidelines are linked, not bundled, as is the 200A/300A probe and signal reference (https://docs.pltcloud.com/design/signals/).

## Test Design

Source: `design/`

Guidelines for designing DUT Production Tests with PLT-based fixtures.

## What to Test ?

Source: `design/what/`

Guidelines for determining what needs to be tested in a DUT during production.

- Test Requirements can be derived from:

   - Design documentation
   - Design reviews (FMEA, DFMEA)

**Scope**

Not all DUT test procedures identified during the design of the DUT Test planning may be suitable for testing in a specific test station.

- Design Validation Testing vs Production Line Testing:

   Some tests might only have to be performed once, to validate the design of a DUT. Such tests could potentially be time-consuming and sometimes destructive, and are best handled as part of a System Design Validation Test of the DUT, instead of during Production Line Testing.

- Production Line Testing vs Production Fault Inspection:

   A test fixture meant for use in a Production Line Test Station is expected to quickly return a PASS or FAIL test outcome, with failing units taken out of the line for Fault Inspection and/or rework.

- Fault Inspection vs Fault Analysis

   A Production Fault Inspection station may only have to identify failing subsystems of the DUT, where actual root cause analysis of the failure may require additional instruments, software or tooling.

**Adaptive Quality Control (AQC)**

By analyzing Test Reports from a previous production run, test plans can be updated to cater for:

- Updated electrical measurement acceptance ranges
- Additional test step items to capture more details on defects found during production
- Removal of redundant test steps that did not uncover production errors

## Design for Test: Board Design

Source: `design/dft-board/`

Not bundled; see https://docs.pltcloud.com/design/dft-board/.

## Design for Test: Firmware

Source: `design/dft-firmware/`

Not bundled; see https://docs.pltcloud.com/design/dft-firmware/.

## PPC Design Guidelines

Source: `design/ppc-guidelines/`

Not bundled; see https://docs.pltcloud.com/design/ppc-guidelines/.

## Design for Manufacturing

Source: `design/dfm/`

Guidelines for DUT design to facilitate manufacturing.
