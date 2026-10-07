import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "simulation"))
import converter_model as cm


def test_buck_duty():
    assert abs(cm.buck_duty(48, 12) - 0.25) < 1e-9


def test_boost_duty():
    assert abs(cm.boost_duty(12, 48) - 0.75) < 1e-9


def test_ripple_buck_positive():
    assert cm.inductor_ripple(48, 12, 0.25, 100e3, 22e-6, "buck") > 0


def test_ripple_boost_positive():
    assert cm.inductor_ripple(12, 48, 0.75, 100e3, 22e-6, "boost") > 0


def test_efficiency_high():
    r = cm.compute_efficiency(48, 12, 1000, "buck")
    assert r.efficiency > 0.93, r.efficiency
    assert r.total > 0


def test_losses_positive():
    r = cm.compute_efficiency(48, 12, 1000, "buck")
    assert r.cond_hs + r.cond_ls + r.sw + r.gate + r.inductor > 0


def test_boost_efficiency():
    r = cm.compute_efficiency(12, 48, 1000, "boost")
    assert r.efficiency > 0.90


def test_rds_rises_with_temp():
    assert cm.rds_on_at_temp(85) > cm.rds_on_at_temp(25)
