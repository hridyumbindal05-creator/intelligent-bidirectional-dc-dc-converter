import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "software"))
import protection as p


def test_no_fault_nominal():
    assert p.check_protection(i12=20, v48=48, v12=12, temp_c=40) == []


def test_overcurrent():
    f = p.check_protection(i12=100, v48=48, v12=12, temp_c=40)
    assert any(x.code == "OVERCURRENT" for x in f)


def test_overtemp():
    f = p.check_protection(i12=20, v48=48, v12=12, temp_c=100)
    assert any(x.code == "OVERTEMP" for x in f)


def test_ov_uv():
    assert any(x.code == "OVERVOLT_48V" for x in p.check_protection(0, 70, 12, 40))
    assert any(x.code == "UNDERVOLT_48V" for x in p.check_protection(0, 20, 12, 40))
    assert any(x.code == "OVERVOLT_12V" for x in p.check_protection(0, 48, 20, 40))


def test_sensor_failure():
    f = p.check_protection(0, 48, 12, 40, sensor_ok=False)
    assert any(x.code == "SENSOR_FAIL" for x in f)
