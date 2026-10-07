# Test Plan

Automated (pytest, `tests/`) + manual/analytical columns:

| ID | Test | File | Status |
|----|------|------|--------|
| T1 | buck duty = Vout/Vin | tests/test_calculations.py | PASS |
| T2 | boost duty = 1−Vin/Vout | tests/test_calculations.py | PASS |
| T3 | ripple positive, modes | tests/test_calculations.py | PASS |
| T4 | efficiency >93 % @1 kW both directions | tests/test_calculations.py | PASS |
| T5 | PI proportional/integral/saturation/reset | tests/test_control.py | PASS |
| T6 | nominal no-fault | tests/test_protection.py | PASS |
| T7 | OC / OV / UV / OT / sensor trips | tests/test_protection.py | PASS |
| T8 | ADC→V/I/T conversions | tests/test_sensors.py | PASS |
| T9 | HIL buck regulates to 12 V | tests/test_hil.py | PASS |
| T10 | HIL boost regulates to 48 V | tests/test_hil.py | PASS |
| T11 | HIL OT + sensor faults | tests/test_hil.py | PASS |
| T12 | FSM direction-change rule | tests/test_hil.py | PASS |
| T13 | HIL load-step stability | tests/test_hil.py | PASS |
| T14 | dashboard sample ranges, CSV roundtrip, summary | tests/test_data_processing.py | PASS |

Run everything with:

```
python -m pytest tests -q
```

Manual/analytical items tracked in `docs/PERFORMANCE_SUMMARY.md` and
`results/efficiency_sweep.csv`.
