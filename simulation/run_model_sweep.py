"""run_model_sweep.py — produce analytical sweep data + plot under results/."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import converter_model as cm

out = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(out, exist_ok=True)

rows = []
for pout in (100, 250, 500, 750, 1000):
    rb = cm.compute_efficiency(48, 12, pout, "buck")
    rs = cm.compute_efficiency(12, 48, pout, "boost")
    rows.append((pout, rb.efficiency, rs.efficiency, rb.total, rs.total))

with open(os.path.join(out, "efficiency_sweep.csv"), "w") as f:
    f.write("pout_w,buck_eff,boost_eff,buck_loss_w,boost_loss_w\n")
    for p, eb, es, lb, ls in rows:
        f.write(f"{p},{eb:.4f},{es:.4f},{lb:.2f},{ls:.2f}\n")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.figure(figsize=(7, 4))
plt.plot([r[0] for r in rows], [r[1] * 100 for r in rows], "o-", label="Buck (CALCULATED)")
plt.plot([r[0] for r in rows], [r[2] * 100 for r in rows], "s-", label="Boost (CALCULATED)")
plt.xlabel("Output power [W]"); plt.ylabel("Efficiency [%]")
plt.title("Calculated efficiency vs. load — analytical model")
plt.grid(True, alpha=0.3); plt.legend(); plt.tight_layout()
p = os.path.join(out, "efficiency_sweep.png")
plt.savefig(p, dpi=120)
print("wrote", p)
for r in rows:
    print(r)
