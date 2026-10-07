import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hil"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "software"))
from hil import HILHarness
from state_machine import ConverterFSM


def test_hil_buck_regulates():
    h = HILHarness("buck")
    log = h.run(0.01)
    t, D, v12, vbat, iL, temp, state, status = log[-1]
    assert status == "OK"
    assert abs(v12 - 12.0) < 0.5
    assert state == "BUCK"


def test_hil_boost_regulates():
    h = HILHarness("boost")
    log = h.run(0.01)
    assert log[-1][7] == "OK"
    assert abs(log[-1][3] - 48.0) < 1.0


def test_hil_overtemp_trips():
    h = HILHarness("buck")
    log = h.run(0.001, fault_inject_temp=True)
    assert log[-1][7] == "OVERTEMP"
    assert log[-1][6] == "FAULT"


def test_hil_sensor_failure_trips():
    h = HILHarness("buck")
    log = h.run(0.001, sensor_fail=True)
    assert log[-1][7] == "SENSOR_FAIL"


def test_fsm_direction_change_requires_idle():
    f = ConverterFSM()
    f.request_mode("buck")
    assert not f.request_mode("boost")  # must go via IDLE
    f.request_mode("idle")
    assert f.request_mode("boost")


def test_fsm_fault_blocks():
    f = ConverterFSM()
    f.request_mode("buck")
    f.trip("OV")
    assert not f.request_mode("boost")
    f.recover()
    f.reset()
    assert f.request_mode("boost")


def test_hil_load_step_stable():
    h = HILHarness("buck")
    log = h.run(0.02, load_R_final=0.72)
    assert log[-1][7] == "OK"
    assert abs(log[-1][2] - 12.0) < 1.0
