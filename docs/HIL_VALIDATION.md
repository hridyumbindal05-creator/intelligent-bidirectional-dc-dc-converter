# HIL Validation

**Classification:** SOFTWARE HIL / controller-in-the-loop / emulation.
Not a physical HIL rig. No FPGA, no power-HIL, no real-time target.

## Plant model (hil/hil.py)

Averaged state-space model:

- Buck: `diL = (Vbat·D − V12)/L`, `dV12 = (iL − V12/Rload)/C12`
- Boost: `diL = (V12 − Vbat·(1−r))/L`, `dVbat = (iL·(1−r) − Vbat/Rbat)/Cbat`
- Thermal: first-order `T''` driven by conduction loss estimate
- dt = 2 µs integration step, t_end typically 10–20 ms

## Controller-in-the-loop

The same PI (kp, ki, anti-windup), FSM and protection logic as the
firmware (Python mirrors under `software/`) runs against the plant.

## Automated scenarios (tests/test_hil.py)

| Scenario | Expected | Result |
|----------|----------|--------|
| Buck startup to regulation | V12 → 12.0 V, D ≈ 0.25 | PASS |
| Boost startup to regulation | Vbat → 48.0 V, r ≈ 0.75 | PASS |
| Load step (buck) | V12 recovers, no trip | PASS |
| Overtemperature injection | FAULT/OT | PASS |
| Sensor failure injection | FAULT/SENSOR_FAIL | PASS |
| Direction change buck→boost | blocked until IDLE | PASS |
| Fault blocks new mode | True | PASS |

## Run it

```
python -c "import sys; sys.path.insert(0,'hil'); from hil import HILHarness; h=HILHarness('buck'); print(h.run(0.01)[-1])"
```

## Honest limitations

- Averaged model, not switching — cannot reproduce EMI, dead-time
  shoot-through transients, or sub-µs ringing.
- "Hardware measured" column in PERFORMANCE_SUMMARY stays empty until a
  physical prototype exists.
