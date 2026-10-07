import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "software"))
import sensors


def test_adc_full_scale():
    assert abs(sensors.adc_to_volts(4095) - 3.3) < 1e-3


def test_bus_voltage():
    # 48 V bus through divider 10 -> adc pin sees 4.8 V? no: divider scales to ~3.3 V max
    # choose operating point: 48/10 = 4.8 V -> beyond VREF; use raw for 33 V: 33/10=3.3 V
    raw = 4095.0 * (33.0 / sensors.DIV_HIGH / 3.3)
    v = sensors.bus_voltage_from_adc(raw, sensors.DIV_HIGH)
    assert abs(v - 33.0) < 0.5


def test_current():
    # 20 A across 1 mOhm with gain 20 -> 0.4 V at adc
    raw = 0.4 / 3.3 * 4095 + 2048
    i = sensors.current_from_adc(raw, 2048)
    assert abs(i - 20) < 1.0


def test_temp_25c():
    # NTC=100k at 25 C, R_SERIES=10k -> Vadc = 3.3 * 100/(100+10)
    raw = (3.3 * 100.0 / 110.0) / 3.3 * 4095.0
    t = sensors.ntc_temp_c(raw)
    assert abs(t - 25.0) < 1.0
