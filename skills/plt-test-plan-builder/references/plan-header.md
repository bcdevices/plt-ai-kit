# Plan Header: Test Station BOM and Wiring

Open every plan with a comment header that lists the test station
equipment and how it is wired. The wiring table always has these five
columns, one row per cable, so it maps 1:1 to a YAML list of records:

```yaml
# -----------------------------------------------------------------------------
# BOM - Test Station
# -----------------------------------------------------------------------------
# SKU    | Model No.            | Model Name
# -------|----------------------|---------------------------
# SKU-6  | PLT-106              | Production Line Tool
# SKU-7  | PER-101              | Test Agent
# SKU-28 | PER-401              | Flashr
# SUB-67 | Bento Board 2        | Device Under Test

# -----------------------------------------------------------------------------
# Test Station Diagram (TSD)
# -----------------------------------------------------------------------------
# Device A | Connector          | Cable P/N          | Connector          | Device B
# ---------|--------------------|--------------------|--------------------|---------
# SKU-6    | USB-A (Port 1)     | TBD                | USB-C (PLT port)   | SKU-7
# SKU-7    | USB-A (Port 2)     | TBD                | USB                | SKU-28
# SKU-28   | 20-pin Header      | TBD                | J1 Tag-Connect     | SUB-67
```

- **Device A / Device B**: the BOM SKU, or the Model No. when the SKU is `—`.
  Every device in the TSD has a BOM row.
- **Connector**: the connector on that device, with the port number or
  reference designator when there is more than one.
- **Cable P/N**: the part number only; the connector columns describe the
  cable's ends. `TBD` if not yet assigned, `—` for a direct connection with
  no cable.
- Order rows from the PLT outward. Don't add other columns or describe the
  wiring in prose instead; put jumper settings and boot-mode notes in
  separate comments.
