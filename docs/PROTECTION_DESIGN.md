# Protection Design

## Strategy

Layered protection — every fault eventually reaches the FSM and pulls both
gates low within one control cycle:

1. **Sensor plausibility** — ADC rail check on V48/V12/IL/T (open/short
   NTC, wire-off) → `FAULT_SENSOR`.
2. **Overcurrent** — IL > ±90 A on the 12 V rail → `FAULT_OC`, gates off.
3. **Overvoltage / undervoltage** — V48 outside 32–62 V; V12 outside
   9.5–14.5 V → `FAULT_UV48/FAULT_OV48/FAULT_UV12/FAULT_OV12`.
4. **Overtemperature** — NTC > 85 °C → `FAULT_OT`.
5. **Shoot-through (design)** — hardware dead-time 200 ns via HRTIM +
   U1's interlock; complementary outputs can never be on together.
6. **Startup fault** — if precharge target not reached, FSM stays in
   PRECHARGE/STARTUP and no gate drive is enabled.
7. **Safe direction change** — BUCK→BOOST requires IDLE (both gates off
   for ≥ 10 ms settle before reverse enable).
8. **Shutdown** — both gates low, PI reset, telemetry posts fault code.
9. **Recovery** — operator must request SHUTDOWN then IDLE before restart;
   fault latches until cleared.

## Threshold table

| Parameter | Threshold | Status |
|-----------|-----------|--------|
| OC limit | ±90 A | DESIGN TARGET |
| OV 48 V | 62 V | DESIGN TARGET |
| OV 12 V | 14.5 V | DESIGN TARGET |
| UV 48 V | 32 V | DESIGN TARGET |
| UV 12 V | 9.5 V | DESIGN TARGET |
| OT | 85 °C (heatsink) | DESIGN TARGET |

## Code parity

Thresholds live in `software/protection.py:THRESH` and
`firmware/Protection/protection.h` — kept identical on purpose; the pytest
suite verifies each branch.
