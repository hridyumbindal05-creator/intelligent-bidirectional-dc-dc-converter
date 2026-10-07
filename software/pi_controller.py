"""pi_controller.py — discrete PI with anti-windup (mirrors firmware/Control/pi.c)."""
from __future__ import annotations


class PIController:
    def __init__(self, kp: float, ki: float, output_min: float, output_max: float,
                 dt: float):
        self.kp = kp
        self.ki = ki
        self.output_min = output_min
        self.output_max = output_max
        self.dt = dt
        self.integral = 0.0

    def reset(self) -> None:
        self.integral = 0.0

    def update(self, setpoint: float, measurement: float) -> float:
        error = setpoint - measurement
        self.integral += error * self.dt
        # anti-windup clamp
        u_unsat = self.kp * error + self.ki * self.integral
        u = min(max(u_unsat, self.output_min), self.output_max)
        if u != u_unsat:
            # conditional integration: back out the saturated increment
            delta = (u - u_unsat) / (self.ki if self.ki != 0 else 1e-9)
            self.integral += delta
            u_unsat = self.kp * error + self.ki * self.integral
            u = min(max(u_unsat, self.output_min), self.output_max)
        return u
