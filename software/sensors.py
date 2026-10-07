"""sensors.py — ADC/sensor conversion (Python mirror of firmware/Sensors)."""
from __future__ import annotations

ADC_MAX = 4095.0
VREF = 3.3

# Voltage sense dividers (must match firmware/Sensors/sensors.h and BOM)
DIV_HIGH = 10.0          # 48 V bus via 100k/10.1k style divider -> scale ~10
DIV_LOW = 4.4255         # 12 V bus via 33k/10k style divider
SHUNT_GAIN = 20.0        # INA240 gain
SHUNT_OHM = 0.001        # 1 mOhm current shunt
NTC_BETA = 3950.0
NTC_NOMINAL = 100e3
T_NOMINAL = 298.15       # 25 C in K
R_SERIES = 10e3


def adc_to_volts(raw: float) -> float:
    return (raw / ADC_MAX) * VREF


def bus_voltage_from_adc(raw: float, divider: float) -> float:
    return adc_to_volts(raw) * divider


def current_from_adc(raw: float, vref_offset_raw: float) -> float:
    v_adc = adc_to_volts(raw - vref_offset_raw)
    return v_adc / (SHUNT_GAIN * SHUNT_OHM)


def ntc_temp_c(raw: float) -> float:
    v = adc_to_volts(raw)
    if v <= 0 or v >= VREF:
        raise ValueError("NTC rail saturation")
    r_ntc = R_SERIES * v / (VREF - v)
    import math
    inv_t = (1.0 / T_NOMINAL) + (1.0 / NTC_BETA) * math.log(r_ntc / NTC_NOMINAL)
    return (1.0 / inv_t) - 273.15


def sensor_plausible(v: float, vmin: float, vmax: float) -> bool:
    return vmin <= v <= vmax
