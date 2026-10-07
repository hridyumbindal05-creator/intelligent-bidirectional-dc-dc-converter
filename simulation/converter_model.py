"""
converter_model.py
Analytical (averaged) engineering model of the synchronous bidirectional
half-bridge DC-DC converter.

All values produced by this file are CALCULATED / ANALYTICAL unless stated
otherwise. This is not a replacement for a SPICE transient simulation; a
matching LTspice netlist is provided in simulation/converter.cir and the
cross-checks are documented in simulation/SIMULATION_RESULTS.md.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Single consistent specification used across docs / firmware / simulation.
# ---------------------------------------------------------------------------
SPEC = {
    "topology": "Synchronous bidirectional half-bridge (buck/boost)",
    "vin_batt_nom": 48.0,      # V, battery port nominal
    "vin_batt_min": 36.0,      # V
    "vin_batt_max": 60.0,      # V
    "vout_dc_nom": 12.0,       # V, 12 V bus port nominal
    "vout_dc_min": 10.8,       # V (±10 %)
    "vout_dc_max": 13.2,       # V
    "p_nom": 1000.0,           # W
    "i_12v_max": 83.3,         # A, 12 V side max (1000 W / 12 V)
    "fs": 100_000.0,           # Hz
    "L": 22e-6,                # H
    "C_12v": 470e-6,           # F (low-voltage output/input bulk)
    "C_48v": 220e-6,           # F (high-voltage side bulk)
    "Rds_on": 5e-3,            # Ohm, per MOSFET (both devices)
    "tr_ns": 25e-9,            # s
    "tf_ns": 25e-9,            # s
    "Qg": 45e-9,               # C, total gate charge
    "Vgate": 10.0,             # V
    "DCR": 2e-3,               # Ohm, inductor winding resistance
    "ESR_out": 5e-3,           # Ohm, output cap ESR
    "rds_temp_coeff": 0.005,   # 1/K (Rds_on increase per deg above 25C)
}


def buck_duty(vin: float, vout: float) -> float:
    """Ideal buck duty cycle Vout/Vin."""
    if vin <= 0:
        raise ValueError("vin must be positive")
    return vout / vin


def boost_duty(vin: float, vout: float) -> float:
    """Ideal boost duty cycle 1 - Vin/Vout."""
    if vin <= 0 or vout <= 0:
        raise ValueError("voltages must be positive")
    return 1.0 - vin / vout


def inductor_ripple(vin: float, vout: float, d: float, fs: float, L: float, mode: str) -> float:
    """Peak-to-peak inductor current ripple [A]."""
    if mode == "buck":
        return (vin - vout) * d / (L * fs)
    if mode == "boost":
        return vin * d / (L * fs)
    raise ValueError("mode must be 'buck' or 'boost'")


def output_voltage_ripple(delta_il: float, C: float, fs: float, esr: float) -> float:
    """Approximate output ripple [V] = capacitive term + ESR term."""
    return delta_il / (8.0 * C * fs) + (delta_il / 2.0) * esr


def mosfet_conduction_loss(i_rms: float, d: float, rds: float) -> float:
    """One MOSFET channel conduction loss; caller sums for both devices."""
    return i_rms ** 2 * rds * d


def mosfet_switching_loss(v: float, i: float, tr: float, tf: float, fs: float) -> float:
    """E = 0.5*V*I*(tr+tf) per cycle."""
    return 0.5 * v * i * (tr + tf) * fs


def gate_drive_loss(Qg: float, Vg: float, fs: float) -> float:
    return Qg * Vg * fs


def inductor_loss(i_rms: float, dcr: float) -> float:
    return i_rms ** 2 * dcr


@dataclass
class LossResult:
    cond_hs: float = 0.0
    cond_ls: float = 0.0
    sw: float = 0.0
    gate: float = 0.0
    inductor: float = 0.0
    total: float = 0.0
    efficiency: float = 0.0
    details: dict = field(default_factory=dict)


def compute_efficiency(vin: float, vout: float, pout: float, mode: str,
                       spec: dict = SPEC) -> LossResult:
    """Full loss budget for one operating point (buck: battery->12V,
    boost: 12V->battery)."""
    fs, L = spec["fs"], spec["L"]
    i_out = pout / vout
    d = buck_duty(vin, vout) if mode == "buck" else boost_duty(vin, vout) \
        if mode == "boost" else None
    if d is None:
        raise ValueError("mode must be 'buck' or 'boost'")
    i_L = i_out / (1 - d) if mode == "boost" else i_out
    dil = inductor_ripple(vin if mode == "buck" else vout,
                          vout if mode == "buck" else vin, d, fs, L, mode)
    i_L_rms = math.sqrt(i_L ** 2 + dil ** 2 / 12.0)
    rds = spec["Rds_on"]
    cond_hs = mosfet_conduction_loss(i_L_rms, d, rds)
    cond_ls = mosfet_conduction_loss(i_L_rms, 1 - d, rds)
    sw = mosfet_switching_loss(vout, i_L, spec["tr_ns"], spec["tf_ns"], fs) * 2  # both devices share events
    gate = gate_drive_loss(spec["Qg"], spec["Vgate"], fs) * 2
    ind = inductor_loss(i_L_rms, spec["DCR"])
    total = cond_hs + cond_ls + sw + gate + ind
    eff = pout / (pout + total)
    return LossResult(cond_hs, cond_ls, sw, gate, ind, total, eff,
                      {"D": d, "i_L": i_L, "dil": dil, "i_L_rms": i_L_rms})


def rds_on_at_temp(t_c: float, rds_25: float = SPEC["Rds_on"],
                   alpha: float = SPEC["rds_temp_coeff"]) -> float:
    return rds_25 * (1 + alpha * (t_c - 25.0))
