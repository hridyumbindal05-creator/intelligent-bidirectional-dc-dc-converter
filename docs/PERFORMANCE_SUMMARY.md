# Performance Summary

| Parameter | Target | Calculated | Simulated | Hardware Measured | Status |
|-----------|--------|-----------|-----------|-------------------|--------|
| Topology | Bidirectional synchronous half-bridge | Implemented in model | HIL verified | — | DESIGNED/HIL |
| Input voltage (battery) | 48 V nom | 48 V | 48.0 V (HIL) | — | SOFTWARE TESTED |
| Output voltage (12 V rail) | 12 V ±10 % | regulates | 12.007 V (HIL) | — | SOFTWARE TESTED |
| Power rating | 1 kW | modeled at 1 kW point | — | — | CALCULATED |
| Switching frequency | 100 kHz | 100 kHz | 100 kHz | — | DESIGNED |
| Inductor | 22 µH shielded | ΔIL≈4.1 A p-p | per netlist | — | CALCULATED/DESIGNED |
| MOSFETs | 100 V, ≤5 mΩ | Q1/Q2 loss ~8.7/26 W | — | — | CALCULATED |
| Efficiency @1 kW buck | > 94 % | 94.9 % | — | — | CALCULATED |
| Efficiency @1 kW boost | > 93 % | 93.6 % | — | — | CALCULATED |
| V12 ripple | < 1 % | ~21 mV | per netlist | — | CALCULATED |
| Dead-time | ≥ 150 ns | 200 ns | — | — | DESIGNED |
| OC trip | 90 A | 90 A | trips (HIL) | — | SOFTWARE TESTED |
| OV trip 48 V | 62 V | 62 V | — | — | DESIGNED |
| UV trip 48 V | 32 V | 32 V | trips (HIL) | — | SOFTWARE TESTED |
| OT trip | 85 °C | 85 °C | trips (HIL) | — | SOFTWARE TESTED |
| PCB | 4-layer, DRC clean | — | — | — | DESIGNED (DRC NOT RUN) |
| Firmware | modular, STM32G4 | — | mirrors tested | — | SOFTWARE TESTED (logic) |
| HIL | software HIL | — | buck/boost/faults | — | HIL/EMULATED |

**Honest note:** the Hardware Measured column is intentionally empty
throughout — no physical prototype or measurement data exists.
