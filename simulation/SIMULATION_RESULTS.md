# Simulation Results

**Status:** The LTspice binary is not installed in this environment, so a
real SPICE transient run was **not** performed. What exists instead:

1. `simulation/converter.cir` — an LTspice-ready synchronous-buck netlist
   that can be opened and run verbatim in LTspice 24 (`.tran 0 5m 3m 1n uic`).
2. `simulation/converter_model.py` — an averaged analytical model used to
   verify the same physics numerically. All outputs below are ANALYTICAL.
3. `hil/hil.py` — a closed-loop controller-in-the-loop run (software HIL),
   results in `docs/HIL_VALIDATION.md`.

## Analytical verification matrix (12-point checklist)

| # | Item | Method | Result |
|---|------|--------|--------|
| 1 | Startup | HIL: PI feedforward D_ff, v12 sweeps to 12 V | software-tested ✓ |
| 2 | Steady state | HIL terminal values | v12 12.007 V, iL 8.3 A, OK ✓ |
| 3 | Buck operation | HIL state BUCK, D≈0.25 | ✓ |
| 4 | Boost operation | HIL state BOOST, D≈0.75, vbat≈48 V | ✓ |
| 5 | Load step | HIL load_R halved at 10 ms | v12 stays within 1 V ✓ |
| 6 | Input variation | duty D=V12/Vbat recalculates in steady state | ✓ (model) |
| 7 | Output regulation | PI holds v12/vbat to refs | ✓ |
| 8 | Inductor ripple | ΔIL = (Vin−Vout)D/Lf | 4.1 A p-p ✓ |
| 9 | Voltage ripple | ΔV = ΔIL/8Cf + ΔIL·ESR/2 | ~21 mV ✓ |
| 10 | Current ripple | same as #8 | 4.1 A p-p ✓ |
| 11 | Switching behavior | dead-time 200 ns margin vs ~50 ns tr/tf | ✓ (design rule) |
| 12 | Efficiency | loss budget | 94.9 % buck / 93.6 % boost @1 kW ✓ |
| 13 | Fault conditions | OC/OV/UV/OT/sensor injection | FSM trips, tests pass ✓ |

## Cross-check vs LTspice netlist

The netlist uses the same 22 µH, 470 µF, 48 V, 12 V, 100 kHz, D=0.25
parameters as the analytical model — running `converter.cir` in LTspice
should reproduce ΔIL ≈ 4 A p-p and Vout ripple in the tens-of-mV range.
That verification is RECOMMENDED FUTURE WORK.
