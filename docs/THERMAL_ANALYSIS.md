# Thermal Analysis (CALCULATED)

## Semiconductor loss @ 1 kW, buck mode

| Source | Value |
|--------|-------|
| Q1 conduction (25 % duty) | 8.7 W |
| Q2 conduction (75 % duty) | 26.0 W |
| Switching (both devices) | 5.0 W |
| Gate drive (both devices) | 0.09 W |
| **Total semiconductor loss** | **≈ 39.8 W** |

## Junction temperature estimate

Assume:
- TO-263 package with PCB copper area 25 cm² → Rth,JA ≈ 40 °C/W per device
  without heatsink (conservative, JEDEC board)
- Ambient Ta = 40 °C
- Q2 (worst case) dissipates ~26 W → ΔT ≈ 26 × 40 = 1040 °C →
  clearly thermally infeasible without a heatsink.

With a modest clip-on heatsink / thick-copper power plane giving
Rth,JA ≈ 5 °C/W:

| Device | Loss | ΔT above ambient | Tj estimate |
|--------|------|------------------|-------------|
| Q1 | ~10.4 W | 52 °C | ≈ 92 °C |
| Q2 | ~26.9 W | 135 °C | ≈ 175 °C ⚠ too high |

With forced-air heatsink Rth,JA ≈ 2.5 °C/W (CALCULATED requirement):

| Device | Tj estimate |
|--------|-------------|
| Q1 | ≈ 66 °C |
| Q2 | ≈ 107 °C → use Vth-derated parts or parallel MOSFETs |

## Recommendation

- Q2 (low-side, highest conduction loss) should either use a lower-Rds part,
  a second parallel MOSFET, or a properly sized forced-air heatsink.
- Target Rth,JC ≤ 1.0 °C/W + thermal vias + Rth,SA ≤ 1.5 °C/W.
- Maximum junction temperature design point: 125 °C (with 25 °C margin
  from a typical 150/175 °C Tj,max).
- Temperature margin tracked at runtime via NTC + FAULT at 85 °C
  (heatsink surface), which corresponds to a junction roughly 20–30 °C hotter.

All values CALCULATED. No hardware was measured.
