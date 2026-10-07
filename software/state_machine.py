"""state_machine.py — converter supervisory state machine."""
from __future__ import annotations
from enum import Enum, auto


class State(Enum):
    IDLE = auto()
    PRECHARGE = auto()
    STARTUP = auto()
    BUCK = auto()      # battery -> 12 V
    BOOST = auto()     # 12 V -> battery
    FAULT = auto()
    SHUTDOWN = auto()


class DirChange:
    """Direction change must pass through IDLE (safe-direction-change rule)."""


class ConverterFSM:
    def __init__(self):
        self.state = State.IDLE
        self.fault_code = None

    def request_mode(self, mode: str) -> bool:
        m = mode.lower()
        if self.state == State.FAULT:
            return False
        if m == "buck" and self.state in (State.IDLE, State.STARTUP, State.BUCK):
            self.state = State.BUCK
            return True
        if m == "boost" and self.state in (State.IDLE, State.STARTUP, State.BOOST):
            self.state = State.BOOST
            return True
        if m == "idle":
            self.state = State.IDLE
            return True
        # cross-transition buck<->boost requires going back to IDLE first
        if m in ("buck", "boost") and self.state in (State.BUCK, State.BOOST):
            return False
        return False

    def start(self) -> None:
        if self.state == State.IDLE:
            self.state = State.PRECHARGE

    def precharge_done(self) -> None:
        if self.state == State.PRECHARGE:
            self.state = State.STARTUP

    def startup_done(self, mode: str) -> None:
        if self.state == State.STARTUP:
            self.request_mode(mode)

    def trip(self, code: str) -> None:
        self.fault_code = code
        self.state = State.FAULT

    def recover(self) -> None:
        if self.state == State.FAULT:
            self.state = State.SHUTDOWN

    def reset(self) -> None:
        self.state = State.IDLE
        self.fault_code = None
