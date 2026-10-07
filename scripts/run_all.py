"""run_all.py — one-command smoke verification of the whole project."""
import subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd):
    print(f"\n$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=ROOT)
    return r.returncode

steps = [
    ("pytest", [sys.executable, "-m", "pytest", "tests", "-q"]),
    ("HIL", [sys.executable, "hil/hil.py"]),
    ("efficiency sweep", [sys.executable, "simulation/run_model_sweep.py"]),
    ("mock dashboard", [sys.executable, "software/dashboard.py", "--headless", "--samples", "50"]),
]
fails = 0
for name, cmd in steps:
    rc = run(cmd)
    print(f"[{name}] exit {rc}")
    if rc != 0:
        fails += 1
print(f"\n{len(steps) - fails}/{len(steps)} steps OK")
sys.exit(1 if fails else 0)
