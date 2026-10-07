# Control System

## Architecture

```
            ┌────────────┐    duty     ┌──────────┐
 Vref ─────►│  PI + A/W  ├────────────►│  HRTIM   │────► Gate driver U1
            └─────▲──────┘             │ PWM+DT   │
                  │                    └──────────┘
        ┌─────────┴──────────┐
        │ ADC (V12/V48/IL/T) │
        └─────────▲──────────┘
        voltage/current/temperature sensors
```

- Voltage-mode PI regulation of V12 (buck) or Vbat (boost)
- Anti-windup via conditional integration clamp (software/pi_controller.py,
  firmware/Control/pi.c)
- Duty feedforward: D_ff = V12/Vbat (buck), D_ff = 1 − V12/Vbat (boost);
  PI trims around this operating point
- ADC sampling synchronous with PWM midpoint (design intent; code stub in
  main.c is executed from the ADC-EOC interrupt hook)
- Complementary PWM with 200 ns dead-time via STM32G4 HRTIM

## State machine (firmware/Core/state_machine.c)

```
IDLE → PRECHARGE → STARTUP → BUCK
                         └→ BOOST
BUCK ⇄ BOOST must transition via IDLE (safe direction change)
any state → FAULT (on protection trip) → SHUTDOWN → IDLE
```

## Soft start

PI integral is initialized to `D_ff/ki` so duty ramps from the analytical
operating point instead of zero/one, then the reference itself is ramped
0→100 % over ~50 ms (implemented in HIL harness via D_ff initialization).

## Current limit

Software OC clamp at 90 A trips the FSM to FAULT within one control cycle
(≈2 µs sampling in target). A hardware-style cycle-by-cycle current limit
via INA240 comparator is RECOMMENDED for the production board.

## Protection hooks

| Fault | Threshold | Action |
|-------|-----------|--------|
| Overcurrent | > 90 A | trip → FAULT |
| Overvoltage 48 V | > 62 V | trip → FAULT |
| Overvoltage 12 V | > 14.5 V | trip → FAULT |
| Undervoltage 48 V | < 32 V | trip → FAULT |
| Undervoltage 12 V | < 9.5 V | trip → FAULT |
| Overtemperature | > 85 °C | trip → FAULT |
| Sensor failure | implausible ADC | trip → FAULT |

Recovery requires the operator to request shutdown then idle.
