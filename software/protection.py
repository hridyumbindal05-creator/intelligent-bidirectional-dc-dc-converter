"""protection.py — protection threshold logic (mirrors firmware/Protection)."""
from __future__ import annotations
from dataclasses import dataclass

THRESH = {
    "oc_current": 90.0,        # A (12 V side), ~1.08x 83.3 A max
    "ov_48v": 62.0,            # V
    "ov_12v": 14.5,            # V
    "uv_48v": 32.0,            # V
    "uv_12v": 9.5,             # V
    "ot_temp": 85.0,           # C
    "sensor_v_min": 0.2,       # V at adc pin — below/above = sensor fault
    "sensor_v_max": 3.1,
}


@dataclass
class Fault:
    code: str
    active: bool = True


def check_protection(i12: float, v48: float, v12: float, temp_c: float,
                     sensor_ok: bool = True) -> list:
    faults = []
    if not sensor_ok:
        faults.append(Fault("SENSOR_FAIL"))
    if abs(i12) > THRESH["oc_current"]:
        faults.append(Fault("OVERCURRENT"))
    if v48 > THRESH["ov_48v"]:
        faults.append(Fault("OVERVOLT_48V"))
    if v12 > THRESH["ov_12v"]:
        faults.append(Fault("OVERVOLT_12V"))
    if v48 < THRESH["uv_48v"]:
        faults.append(Fault("UNDERVOLT_48V"))
    if v12 < THRESH["uv_12v"]:
        faults.append(Fault("UNDERVOLT_12V"))
    if temp_c > THRESH["ot_temp"]:
        faults.append(Fault("OVERTEMP"))
    return faults
