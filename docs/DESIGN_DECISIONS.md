# Design Decisions

| Decision | Rationale / Value |
|----------|-------------------|
| Topology | Synchronous bidirectional half-bridge with single inductor — simplest bidirectional buck/boost, synchronous rectification minimizes loss |
| Battery port | 48 V nominal, 36–60 V operating window (EV 48 V mild-hybrid class bus) |
| 12 V bus port | 12 V ±10 % (automotive 12 V rail) |
| Power rating | 1 kW continuous (83 A on 12 V side, ~21 A battery side) |
| Switching frequency | 100 kHz — good balance of magnetics size, switching loss, and control bandwidth |
| Inductor | 22 µH, 25 A saturation, shielded — ΔIL ≈ 4 A p-p at 48→12 V, 100 kHz |
| MOSFETs | 100 V, ≤5 mΩ Rds(on), TO-263 — VDS margin ≥1.6× over 60 V max bus |
| Gate driver | Half-bridge driver, 200 ns dead-time, boot-strapped HS channel |
| Current sensing | INA240 gain-20 + 1 mΩ shunt (Kelvin-connected), low-side placement |
| Voltage sensing | Resistive dividers (10:1 on 48 V, ~4.43:1 on 12 V) + ADC anti-alias RC |
| Temperature | 100 kΩ NTC (β=3950) on MOSFET heatsink + single-ADC conversion |
| MCU | STM32G474 — HRTIM for dead-time-insertion PWM, fast ADC, suitable for GS/CMC |
| Control | Voltage-mode PI per direction, feedforward duty, anti-windup clamp |
| Protection | Hardware-style thresholds on OC/OV/UV/OT + sensor-plausibility checks + FSM latch |
| PCB | 4-layer: L1 signal/gate, L2 GND plane, L3 power plane, L4 signal. Kelvin sense routing, thermal vias under TO-263 |
| HIL | Software-based controller-in-the-loop only (not physical HIL) |

Single source of truth: `simulation/converter_model.py:SPEC` — firmware
headers, Python model, BOM, and all docs reference these numbers.
