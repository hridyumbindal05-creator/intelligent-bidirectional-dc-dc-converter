"""dashboard.py — Python monitoring dashboard.

MOCK/SIMULATION mode by default (no physical serial hardware exists yet).
Use --headless to write data/telemetry_*.csv and print summary statistics
without opening the GUI. Use --gui to launch the tkinter dashboard.
"""
from __future__ import annotations
import argparse, csv, math, os, random, sys, time
from dataclasses import dataclass, asdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hil"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "software"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "simulation"))


@dataclass
class Sample:
    t: float
    v_in: float
    v_out: float
    i_in: float
    i_out: float
    p_in: float
    p_out: float
    efficiency: float
    temp: float
    mode: str
    fault: str


def mock_sample(t: float, mode: str = "BUCK", seed: int = 0) -> Sample:
    rnd = random.Random(int(t * 1000) + seed)
    v48 = 48.0 + rnd.uniform(-0.2, 0.2)
    v12 = 12.0 + rnd.uniform(-0.1, 0.1)
    i48 = 21.0 + rnd.uniform(-1, 1)
    i12 = 83.0 + rnd.uniform(-3, 3)
    pin = v48 * i48
    pout = v12 * i12
    eff = min(max(pout / pin, 0.0), 0.99) if pin > 0 else 0
    temp = 45 + rnd.uniform(-1, 1)
    return Sample(t, v48, v12, i48, i12, pin, pout, eff, temp, mode, "NONE")


def write_csv(samples, path) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(samples[0]).keys()))
        w.writeheader()
        for s in samples:
            w.writerow(asdict(s))


def summarize(samples) -> dict:
    import statistics as st
    return {
        "v_in_avg": st.mean(s.v_in for s in samples),
        "v_out_avg": st.mean(s.v_out for s in samples),
        "p_out_avg": st.mean(s.p_out for s in samples),
        "eff_avg": st.mean(s.efficiency for s in samples),
        "temp_max": max(s.temp for s in samples),
        "faults": sum(1 for s in samples if s.fault != "NONE"),
    }


def run_headless(n: int = 200, dt: float = 0.05, out: str = None) -> str:
    samples = [mock_sample(i * dt) for i in range(n)]
    out = out or os.path.join(os.path.dirname(__file__), "..", "data", "telemetry_mock.csv")
    write_csv(samples, out)
    return out, summarize(samples)


def run_gui() -> None:
    import tkinter as tk
    from tkinter import ttk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt

    root = tk.Tk()
    root.title("Bidirectional DC-DC Converter — MOCK Telemetry Dashboard")
    fig, axes = plt.subplots(3, 1, figsize=(9, 7))
    fig.tight_layout(pad=2.0)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    status = ttk.Label(root, text="MOCK DATA — no hardware connected", foreground="red")
    status.pack()

    t, v, i, eff, temp = [], [], [], [], []
    start = time.time()

    def update():
        s = mock_sample(time.time() - start)
        t.append(s.t); v.append(s.v_out); i.append(s.i_out)
        eff.append(s.efficiency * 100); temp.append(s.temp)
        t[:], v[:], i[:], eff[:], temp[:] = t[-100:], v[-100:], i[-100:], eff[-100:], temp[-100:]
        for ax in axes: ax.clear()
        axes[0].plot(t, v, label="Vout (V)"); axes[0].legend()
        axes[1].plot(t, i, label="Iout (A)", color="orange"); axes[1].legend()
        axes[2].plot(t, eff, label="Eff (%)", color="green")
        ax2 = axes[2].twinx(); ax2.plot(t, temp, label="Temp (C)", color="red")
        canvas.draw()
        root.after(200, update)

    update()
    root.mainloop()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gui", action="store_true")
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--samples", type=int, default=200)
    args = ap.parse_args()
    if args.gui:
        run_gui()
    else:
        path, stats = run_headless(n=args.samples)
        print(f"Wrote {path}")
        for k, v in stats.items():
            print(f"  {k}: {v:.4g}")
