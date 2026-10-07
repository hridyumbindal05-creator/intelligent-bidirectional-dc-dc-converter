# Resume Entry

## Project Title
Intelligent Bidirectional DC-DC Converter for EV Battery and Energy
Storage Applications

## One-line Description
Designed, modeled, and simulated a 1 kW, 48 V↔12 V bidirectional
synchronous DC-DC converter with closed-loop PI control, sensing,
protection logic, HIL emulation, and a KiCad 4-layer PCB design.

## ATS-friendly bullets

- Designed and simulated a low-voltage bidirectional synchronous DC-DC
  converter with MOSFET power stage, closed-loop PI control, sensing,
  and protection logic; developed the KiCad schematic and 4-layer PCB
  layout with documented DRC status.
- Implemented averaged-state-space analytical models and a software
  controller-in-the-loop (HIL) testbench in Python/NumPy, verifying
  buck/boost regulation, load-step response, and protection trips via a
  31-test automated pytest suite.
- Created a modular STM32 firmware skeleton (HRTIM PWM, ADC, PI, FSM,
  protection, telemetry) mirroring the tested Python reference model,
  plus a mock-mode Python telemetry dashboard with CSV logging.

## Technologies / Tools
Bidirectional DC-DC Converter, Synchronous Converter, MOSFET, Gate
Driver, STM32 (STM32G474 HRTIM), PI Control, KiCad, PCB Layout,
LTspice/SPICE, Thermal Analysis, Protection Design, Software HIL,
Python, pytest, Tkinter/Matplotlib

## Honesty note
No physical hardware was built or measured; all results are CALCULATED,
SIMULATED, or SOFTWARE TESTED. Do not claim bench measurement,
certification, or a flashed prototype.
