# PCB Design

**Status:** 4-layer PCB is a **DESIGN** only. No proof of fabrication
exists. KiCad DRC has NOT been executed (no KiCad binary in this
environment) — running `kicad-cli drc` is required before fabrication.

## Stackup

| Layer | Function |
|-------|----------|
| F.Cu | Components, gate-drive, signal, sense |
| In1.Cu | 12 V power plane (heavy copper pours for power paths) |
| In2.Cu | Solid GND plane — no splits under the power stage |
| B.Cu | Bulk 12 V/48 V routing, test points |

## Power integrity / routing rules (design intent)

- High-current loop Q1–Q2–L1–C2 kept < 25 mm² on F.Cu where feasible
- All GND returns via the In2.Cu plane with via stitching at each port
- Gate-driver traces < 10 mm, no stubs, referenced to the source Kelvin pad
- Current-sense: INA240 inputs routed as a Kelvin pair, no other signals
  within 3 mm
- Voltage dividers close to their test points, RC filtered
- Thermal vias (0.3 mm drill / 6-mil... style) under Q1/Q2 TO-263 tabs
- Decoupling: 100 nF on every IC pin as close as pad-to-pad allows, plus
  1 µF and bulk electrolytics at each port
- Test points: V48, V12, SW, IL (across R3), TEMP, GND

## DRC status

`NOT RUN` in this environment. The `.kicad_pcb` file contains the
placement-critical nets (V48/V12/GND/SW/HO/LO) as a starting definition;
full DRC + ERC is FUTURE WORK with the KiCad GUI.
