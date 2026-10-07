# Interview Preparation

## 30-second project explanation

"I designed a 1 kW bidirectional DC-DC converter that can move power
between a 48 V battery and a 12 V rail. In buck mode it steps the
battery down to 12 V; in boost mode it charges the battery back up. I
worked through the whole flow: topology selection, power-stage design,
PI control, protection, STM32 firmware structure, KiCad schematic and
4-layer PCB, thermal and efficiency analysis, and a software
controller-in-the-loop testbench with an automated pytest suite."

## 1-minute explanation

"The converter is a synchronous half-bridge: two MOSFETs switch a 100
kHz PWM across an inductor connected to each rail. Software direction
pins decide whether it bucks (battery to 12 V) or boosts (12 V to
battery). An STM32G4 generates complementary PWM with 200 ns dead-time
through HRTIM, samples voltage/current/temperature with its ADC, and
runs a PI loop that regulates the output rail around a feedforward
duty. I wrote an analytical loss model that predicts roughly 95 %
efficiency in buck and 94 % in boost at 1 kW, and I built a software
HIL harness with an averaged state-space plant plus the same PI, state
machine, and protection code as the firmware. The pytest suite covers
every protection branch, the direction-change rule, load-step recovery,
and sensor conversions. KiCad schematic and PCB are designed but DRC
and hardware validation are still future work."

## 3-minute technical deep dive

(Expand on: topology choice vs. non-isolated SEPIC/Ćuk; why synchronous
half-bridge for bidirectional; duty-ratio and ripple math (ΔIL ≈ 4 A p-p
at 22 µH, 100 kHz); loss budget (Q1/Q2 conduction vs. D, switching loss
proportional to V·I·fs); dead-time trade-off between shoot-through and
body-diode loss; PI tuning and anti-windup; the state machine's
direction-change-through-IDLE rule; sense design (1 mΩ shunt, INA240
gain 20, Kelvin pair); thermal estimate driving the need for a second
parallel low-side MOSFET or forced-air heatsink; software HIL plant
equations and dt constraints; and honest limitations — averaged model,
no EMI transients, no physical validation.)

## Technical Q&A (30+)

**Q: Buck vs boost — what's the fundamental difference?**
A: Buck steps Vout = D·Vin down with the switch node feeding an LC
filter; boost steps Vout = Vin/(1−D) up by storing energy in the
inductor during switch-on and releasing it to the output during
switch-off. Same inductor, different port reference.

**Q: Why a bidirectional converter instead of two separate converters?**
A: One magnetic, one switch pair, lower cost/weight — and it allows
energy recovery from the 12 V side back to the battery.

**Q: What is synchronous rectification?**
A: Replacing a diode with a MOSFET driven a fraction of a cycle. Its
Rds(on) conduction path is far lower loss than a 0.7 V diode drop —
critical at 83 A.

**Q: How do you select a MOSFET?**
A: Vds ≥ ~1.6× bus max (here 100 V for 60 V max), Rds(on) as low as
practical, gate charge Qg low enough that switching loss Qg·Vg·fs stays
small, and package/Rth,JC for the loss we must dissipate.

**Q: Why is high-side drive harder than low-side?**
A: The high-side source floats at the switch node (0–48 V), so the gate
drive needs a boot-strapped or isolated supply that follows it.

**Q: What is dead-time?**
A: The gap inserted between Q1 turning off and Q2 turning on (and
vice-versa) so they are never on simultaneously. Here 200 ns, long
enough to prevent cross-conduction given ~50 ns worst-case switching.

**Q: What is shoot-through?**
A: Both MOSFETs momentarily on, shorting the bus through ~10 mΩ total —
that is tens of amps of pure loss and potential device failure. Dead-
time plus gate-driver interlock prevents it.

**Q: Switching losses scale as what?**
A: Roughly ½·V·I·(tr+tf)·fs. Doubling frequency doubles switching loss;
it dominates as V and I rise.

**Q: Conduction losses scale as what?**
A: I²·Rds(on)·D per device. Rds(on) rises with temperature (~+0.5 %/°C),
so hot hardware runs less efficient.

**Q: How do you size the inductor?**
A: Choose acceptable ripple ratio (~30 % of Imax ≈ 4 A), then
L = (Vin−Vout)·D/(ΔIL·fs). 22 µH gives 4.1 A p-p here.

**Q: How do you size the output capacitor?**
A: Capacitive ripple ≈ ΔIL/(8·C·fs); with 470 µF that's ~11 mV, plus
ESR ≈ 10 mV — well under the 120 mV budget.

**Q: What is ripple?**
A: The residual AC component on the output voltage/current. It comes
from capacitor charge/discharge and ESR during the inductor's ripple
current.

**Q: What is a PI controller?**
A: P gives immediate response to error; I integrates the error to kill
steady-state offset. Tuned (kp, ki) together for fast, stable duty
commands.

**Q: What is anti-windup?**
A: When the duty output saturates (0–100 %), further integral growth is
blocked/backed out, otherwise recovery overshoots badly. Implemented in
both Python and C.

**Q: How is PWM generated?**
A: A timer (STM32 HRTIM) counts to the period; compare registers set
the duty of the two complementary channels. Midpoint/valley-aligned
mode reduces harmonics.

**Q: Why sample the ADC at the PWM midpoint?**
A: Inductor current is approximately triangular; the midpoint samples
the average current, rejecting ripple-induced noise.

**Q: How does current sensing work?**
A: A 1 mΩ shunt develops 83 mV at 83 A; INA240 amplifies by 20× to
1.66 V for the ADC, with Kelvin connections to avoid PCB-trace drop.

**Q: What is Kelvin sensing?**
A: Dedicated, 4-wire-style force/sense taps at the exact shunt pad so
no current-induced voltage drop corrupts the measurement.

**Q: Walk me through thermal design.**
A: Sum losses per device (conduction + switching), then Tj = Ta + P·Rth.
A bare TO-263 on FR4 has Rth,JA ~ 40 °C/W — impossible at 27 W; a
heatsink/forced air with ~2.5 °C/W is required, still giving Tj ≈ 107 °C
for Q2, which motivates a bigger/paralleled low-side device.

**Q: Key PCB layout rules for a power converter?**
A: Minimize the high-current commutation loop (Q1–Q2–L1–C2), solid GND
plane, Kelvin sense routing away from the SW node, gate traces short
and referenced to source, decoupling at the IC, thermal vias under
power tabs, creepage between 48 V and SELV 12 V domains.

**Q: Sources of EMI?**
A: The SW node's ~2 V/ns edges (CM noise through parasitic capacitance)
and the commutated inductor current loop (near-field H). Mitigations:
smaller loop, gate resistors, snubbers, input π-filters, CM choke at
the port.

**Q: Single-point vs. solid-plane grounding?**
A: At this frequency/power a solid plane is correct; the "single point"
is where the ADC sense returns and the bulk caps reference, to avoid
rippling sensor ground.

**Q: How do you protect from overcurrent?**
A: Software threshold trip to FAULT (90 A) plus a hardware comparator
path in production; the FSM latches until shutdown/reset.

**Q: What does your HIL do that a simulation doesn't?**
A: It runs the *actual controller code* (PI, FSM, protection) against a
plant model, so it validates software behavior — sequencing, fault
edges, direction-change safety — not just the plant physics.

**Q: Why averaged-model HIL and its limits?**
A: Simulation step ~2 µs keeps a 10 ms run in ~5k steps — fast enough
for thousands of CI runs. It cannot capture switching transients, EMI,
or dead-time effects, which remain future work.

**Q: Efficiency target and what limits it?**
A: ~95 %/94 % at 1 kW (calculated). Dominant terms: Q2 low-side
conduction and inductor DCR in buck; switching loss in boost because it
switches at 48 V.

**Q: What testing have you actually run?**
A: 31 pytest tests for control/protection/sensors/HIL/dashboard paths,
an efficiency sweep CSV, and the HIL scenarios. No hardware bench
testing — stated honestly.

**Q: What would you do next?**
A: Run KiCad DRC, fabricate, and close the loop with a real STM32 on the
board; then measure efficiency/ripple/temperatures and re-run the HIL
harness against real telemetry.
