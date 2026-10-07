"""
hil.py — SOFTWARE-BASED HIL / controller-in-the-loop for the bidirectional
converter. NOT physical HIL.

Plant: averaged state-space model of the half-bridge converter with a stiff
source on the "other" rail, a bulk capacitor on the regulated rail, an
inductor state, sensor noise and a temperature model. The same PI/FSM/
protection logic used by the firmware is exercised here.
"""
from __future__ import annotations
import sys, os, math
from dataclasses import dataclass, field

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "software"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "simulation"))

from pi_controller import PIController
from state_machine import ConverterFSM, State
import protection as prot


@dataclass
class PlantState:
    iL: float = 0.0
    v12: float = 12.0
    vbat: float = 48.0
    temp: float = 25.0


class ConverterPlant:
    def __init__(self, mode: str = "buck", fs: float = 100e3, L: float = 22e-6,
                 C12: float = 470e-6, dt: float = 2e-6,
                 load_R: float = 1.44, vbat_src: float = 48.0, v12_src: float = 12.0,
                 Cbat: float = 200.0, rbat: float = 20.0):
        self.mode = mode
        self.fs = fs
        self.L = L
        self.C12 = C12
        self.Cbat = Cbat
        self.dt = dt
        self.load_R = load_R
        self.vbat_src = vbat_src
        self.v12_src = v12_src
        self.rbat = rbat
        self.s = PlantState(v12=v12_src, vbat=vbat_src)

    def step(self, D: float) -> PlantState:
        s = self.s
        i_load = s.v12 / self.load_R
        if self.mode == "buck":
            diL = (self.vbat_src * D - s.v12) / self.L
            dv12 = (s.iL - i_load) / self.C12
        else:  # boost, D = LOW-side duty r; vbat = v12/(1-r) at steady state
            diL = (self.v12_src - s.vbat * (1.0 - D)) / self.L
            s.iL = s.iL + diL * self.dt
            i_bat = s.iL * (1.0 - D)
            s.vbat = s.vbat + (i_bat - s.vbat / self.rbat) / self.Cbat * self.dt
            s.v12 = self.v12_src
            self._temp(s, D)
            return s
        s.iL = s.iL + diL * self.dt
        s.v12 = s.v12 + dv12 * self.dt
        self._temp(s, D)
        return s

    def _temp(self, s: PlantState, D: float) -> None:
        ploss = 0.5 * abs(s.iL) ** 2 * 0.007 + 2.0  # crude: Pcond + quiescent
        s.temp += (ploss * 0.5 - (s.temp - 25.0) * 0.2) * self.dt  # 1st order to ambient


class HILHarness:
    def __init__(self, mode: str = "buck"):
        self.mode = mode
        self.plant = ConverterPlant(mode=mode)
        self.fsm = ConverterFSM()
        self.fsm.request_mode(mode)
        D_ff = 0.25 if mode == "buck" else 0.75
        self.pi = PIController(kp=2e-4 if mode == "buck" else 2e-4,
                               ki=0.5 if mode == "buck" else 0.5,
                               output_min=0.0, output_max=0.9, dt=self.plant.dt)
        self.pi.integral = D_ff / self.pi.ki
        self.ref = 12.0 if mode == "buck" else 48.0  # v12 ref or vbat ref
        self.log = []

    def run(self, t_end: float, load_R_final: float = None,
            fault_inject_temp: bool = False, sensor_fail: bool = False) -> list:
        steps = int(t_end / self.plant.dt)
        for k in range(steps):
            t = k * self.plant.dt
            if load_R_final is not None and t > t_end / 2:
                self.plant.load_R = load_R_final
            if fault_inject_temp:
                self.plant.s.temp = 95.0
            D = self.pi.update(self.ref,
                               self.plant.s.v12 if self.mode == "buck" else self.plant.s.vbat)
            s = self.plant.step(D)
            faults = prot.check_protection(
                i12=s.v12 / self.plant.load_R, v48=s.vbat, v12=s.v12,
                temp_c=s.temp, sensor_ok=not sensor_fail)
            if faults:
                self.fsm.trip(faults[0].code)
                self.log.append((t, D, s.v12, s.vbat, s.iL, s.temp, self.fsm.state.name,
                                 faults[0].code))
                break
            self.log.append((t, D, s.v12, s.vbat, s.iL, s.temp, self.fsm.state.name, "OK"))
        return self.log


if __name__ == "__main__":
    for mode in ("buck", "boost"):
        h = HILHarness(mode)
        last = h.run(0.01)[-1]
        print(f"{mode}: t={last[0]:.4f}s D={last[1]:.3f} v12={last[2]:.3f}V "
              f"vbat={last[3]:.3f}V state={last[6]} status={last[7]}")
