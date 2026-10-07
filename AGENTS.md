# AGENTS.md — guidance for future AI/engineering passes on this repo

## Rules

1. **Never fabricate hardware evidence.** If a value did not come from a
   calculation, analytical model, pytest run, or HIL run it must be
   labeled `CALCULATED`, `SIMULATED`, `SOFTWARE TESTED`, `HIL/EMULATED`,
   or `DESIGNED`. The `Hardware Measured` column stays empty unless a
   real measurement exists.
2. **Single spec source:** `simulation/converter_model.py:SPEC`. Do not
   introduce a different voltage/power/frequency/inductor in any doc,
   firmware header, netlist, or test.
3. Run `python -m pytest tests -q` after any change to `software/`,
   `hil/`, or `simulation/`.
4. Keep Python mirrors (`software/*.py`) and C firmware headers in sync
   (PI gains, protection thresholds, sensor scaling).
5. Do not delete the KiCad/HIL/simulation artifacts to satisfy
   "cleanliness" — they are the engineering record.

## Entry points

- Dashboard: `python software/dashboard.py --headless --samples 200`
  (add `--gui` for the Tkinter view)
- HIL smoke: `python hil/hil.py`
- Efficiency sweep: `python simulation/run_model_sweep.py`
- Tests: `python -m pytest tests -q`
