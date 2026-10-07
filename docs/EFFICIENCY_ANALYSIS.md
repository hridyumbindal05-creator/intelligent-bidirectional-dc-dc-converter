# Efficiency Analysis

All numbers below are **CALCULATED** by `simulation/converter_model.py`
(see `results/efficiency_sweep.csv` and `results/efficiency_sweep.png`).

## Loss budget @ 1 kW, 48 V→12 V (buck, CALCULATED)

| Term | Value |
|------|-------|
| Q1 conduction (D·I²·Rds) | ≈ 8.7 W |
| Q2 conduction ((1−D)·I²·Rds) | ≈ 26.0 W |
| Switching (0.5·V·I·(tr+tf)·fs, both devices) | ≈ 5.0 W |
| Gate drive (Qg·Vg·fs, both devices) | ≈ 0.09 W |
| Inductor I²·DCR | ≈ 13.9 W |
| **Total loss** | **≈ 53.7 W** |
| **Efficiency** | **η ≈ 94.9 %** |

## Loss budget @ 1 kW, 12 V→48 V (boost, CALCULATED)

| Term | Value |
|------|-------|
| Q1 conduction | ≈ 26.0 W |
| Q2 conduction | ≈ 8.7 W |
| Switching | ≈ 20.0 W |
| Gate drive | ≈ 0.09 W |
| Inductor I²·DCR | ≈ 13.9 W |
| **Total loss** | **≈ 68.9 W** |
| **Efficiency** | **η ≈ 93.6 %** |

## Notes

- Switching loss dominates the boost direction because the switch-node
  voltage is 4× higher; expect boost efficiency a few points lower.
- Inductor DCR dominates the mid-band; a lower-DCR (larger) part would
  trade size for a point or two of efficiency.
- These are idealized averaged-model numbers — EMI filter losses, gate
  resistor losses, sense-amp quiescent draw and body-diode dead-time
  conduction are not included. Measured efficiency is FUTURE WORK.
