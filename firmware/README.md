# Firmware

Modular STM32 firmware skeleton for the bidirectional DC-DC converter.

| Module | Files | Status |
|--------|-------|--------|
| Control | Control/pi.c/h | Written, logic-tested via Python mirror |
| Core | Core/state_machine.c/h, Core/main.c | Written, NOT flashed |
| Drivers | Drivers/pwm_driver.c/h | Written (HRTIM mapping documented) |
| Sensors | Sensors/sensors.c/h | Written |
| Protection | Protection/protection.c/h | Written |
| Communication | Communication/telemetry.c/h | Written |

**Honest status:** the code is logically complete and mirrors the Python
reference model tested by the pytest suite. It has NOT been compiled in a
toolchain or flashed onto an STM32. Physical hardware validation remains
future work.
