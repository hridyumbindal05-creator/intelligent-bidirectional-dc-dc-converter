# EMI / EMC

**Scope:** design guidance only. No EMC certification, pre-compliance lab
result, or measured emissions spectrum exists.

## Identified noise sources

- SW node: 48 V swinging in ~25 ns → dv/dt ≈ 2 V/ns → needs control
- Inductor current commutates Q1↔Q2 at 100 kHz with ~4 A p-p ripple →
  di/dt spikes on every commutation
- Gate-drive loop (HO/HS, LO/GND): high di/dt at each edge

## Mitigation strategy

| Technique | Implementation (design intent) |
|-----------|--------------------------------|
| Small switching loop | Q1,Q2,L1,C2 packed; In1/In2 planes pour copper; loop < 25 mm² |
| Gate control | Series gate resistors (4.7–10 Ω) to set tr/tf, optional RC snubber H-L on SW |
| DC-link decoupling | 100 nF 100 V MLCC directly across Q1–Q2 source path, 1 µF near + ferrites at ports |
| Common-mode | Port-side CM choke footprint reserved, Y-cap footprints (to chassis) unpopulated by default |
| Differential-mode | LC input filter footprint + π-filter on 12 V output |
| Grounding | Single solid GND plane, star at the ADC/GND sense point; all returns to the plane |
| Kelvin sensing | Current shunt Kelvin pair, voltage dividers at the test points |
| Shielding | No enclosure modeled in this design phase |
| Pre-compliance | Plan: near-field probing, LISN + 100 kHz–30 MHz CISPR 25-style check before cert lab |

## What we do NOT claim

- No conducted/radiated emissions measurements
- No CISPR 25, IEC 61000, or automotive EMC certification
- No pre-compliance report exists
