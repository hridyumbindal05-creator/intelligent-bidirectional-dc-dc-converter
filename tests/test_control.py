import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "software"))
from pi_controller import PIController


def test_pi_proportional():
    pi = PIController(kp=1.0, ki=0.0, output_min=-100, output_max=100, dt=0.1)
    assert pi.update(10, 0) == 10


def test_pi_integral_accumulates():
    pi = PIController(kp=0.0, ki=1.0, output_min=-100, output_max=100, dt=0.1)
    pi.update(5, 0)
    u = pi.update(5, 0)
    assert abs(u - 1.0) < 1e-9


def test_pi_saturation():
    pi = PIController(kp=100.0, ki=0.0, output_min=0, output_max=0.9, dt=0.1)
    assert pi.update(10, 0) == 0.9


def test_pi_reset():
    pi = PIController(kp=0.0, ki=1.0, output_min=-1, output_max=1, dt=0.1)
    pi.update(1, 0)
    pi.reset()
    assert pi.integral == 0.0
