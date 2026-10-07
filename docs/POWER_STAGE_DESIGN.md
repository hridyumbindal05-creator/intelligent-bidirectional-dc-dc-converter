# Power Stage Design

Topology: synchronous bidirectional half-bridge (buck ↔ boost). High-side
Q1 connects the switch node to the 48 V port, low-side Q2 to ground;
inductor L1 between the switch node and the 12 V port. Q1/Q2 switch
complementarily with ~200 ns dead-time through U1.

## Buck mode (48 V → 12 V)

- Duty: D = Vout/Vin = 12/48 = 0.25
- Average switch node: 0.25 × 48 = 12 V
- Inductor ripple: ΔIL = (48−12)·0.25/(22 µH·100 kHz) ≈ 4.1 A p-p
- Output current: Iout = 1000 W / 12 V ≈ 83 A

## Boost mode (12 V → 48 V)

- Low-side duty: r = 1 − Vin/Vout = 1 − 12/48 = 0.75
- Inductor ripple: ΔIL = 12·0.75/(22 µH·100 kHz) ≈ 4.1 A p-p
- Input current: Iin = 1000 W / 12 V / η ≈ 87 A

## Capacitor ripple check (CALCULATED)

With C12 = 470 µF, ESR 5 mΩ, ΔIL = 4.1 A:
- Capacitive ripple: ΔIL/(8·C·fs) ≈ 4.1/(8·470e-6·1e5) ≈ 10.9 mV
- ESR term: (ΔIL/2)·ESR ≈ 2.05 × 5 mΩ ≈ 10.2 mV
- Total V12 ripple ≈ 21 mV p-p ≪ 120 mV budget (1 %) ✓

## Dead-time / shoot-through

200 ns dead-time versus worst-case MOSFET turn-off ~50 ns leaves ~150 ns
margin; body-diode conduction during dead-time causes a small voltage
error (≈ 0.7 V·200 ns·100 kHz ≈ 14 mV on the LW side) — acceptable.

## Operating envelope

| Quantity | Value |
|----------|-------|
| Vbat nominal | 48 V (36–60 V) |
| V12 nominal | 12 V ±10 % |
| Pnom | 1 kW |
| fs | 100 kHz |
| L | 22 µH |
| Iout,max | 83 A |
| ΔIL | ~4 A p-p |

All values CALCULATED unless otherwise marked.
