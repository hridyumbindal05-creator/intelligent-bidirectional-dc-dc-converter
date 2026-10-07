import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")

boxes = [
    (0.3, 3.2, "48 V Battery"),
    (3.4, 3.2, "Half-bridge\nQ1 / Q2 / U1"),
    (6.5, 3.2, "Inductor L1\n+ caps"),
    (6.5, 1.0, "12 V Bus"),
    (3.4, 1.0, "STM32G474\nHRTIM + ADC + PI"),
    (0.3, 1.0, "Sensors\nV/I/T"),
]
for x, y, t in boxes:
    ax.add_patch(FancyBboxPatch((x, y), 2.4, 1.2, boxstyle="round,pad=0.05",
                                fc="#e8f0fe", ec="#1a73e8"))
    ax.text(x + 1.2, y + 0.6, t, ha="center", va="center", fontsize=10)

arrows = [
    ((2.7, 3.8), (3.4, 3.8)),
    ((5.8, 3.8), (6.5, 3.8)),
    ((7.7, 3.2), (7.7, 2.2)),
    ((5.8, 1.6), (4.1, 1.6)),
    ((3.4, 1.6), (2.7, 1.6)),
    ((1.5, 2.2), (1.5, 3.2)),
    ((4.6, 2.2), (4.6, 3.2)),
]
for (x1, y1), (x2, y2) in arrows:
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=15, color="#444"))

ax.set_title("System architecture — bidirectional DC-DC converter")
plt.tight_layout()
os.makedirs("images", exist_ok=True)
plt.savefig("images/system_architecture.png", dpi=130)
print("ok")
