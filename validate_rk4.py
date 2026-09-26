"""Calibration test for physkit's RK4 integrator.

A mass on a spring has a known exact answer: x(t) = cos(omega*t)
when it starts at x = 1 with zero velocity. We solve it with RK4
at smaller and smaller steps. If RK4 is coded correctly, halving
the step cuts the error by about 16x (2^4 = 16).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")            # save the plot to a file, don't open a window
import matplotlib.pyplot as plt
from physkit.integrators import rk4_integrate

omega = 2.0      # how fast the spring oscillates (rad/s)
T_END = 10.0     # simulate 10 seconds


def spring(t, y):
    x, v = y                          # position, velocity
    return np.array([v, -omega**2 * x])


steps = [0.1, 0.05, 0.025, 0.0125, 0.00625]
errors = []
print(f"{'step h':>10} {'max error':>12} {'ratio':>7}")
for h in steps:
    n = round(T_END / h)
    t, y = rk4_integrate(spring, 0.0, [1.0, 0.0], h, n)
    err = np.max(np.abs(y[:, 0] - np.cos(omega * t)))
    ratio = errors[-1] / err if errors else float("nan")
    errors.append(err)
    print(f"{h:>10.5f} {err:>12.3e} {ratio:>7.2f}")

ratios = [errors[i] / errors[i + 1] for i in range(len(errors) - 1)]
if all(14 < r < 18 for r in ratios):
    print("\nPASS: error falls ~16x per halving -> 4th-order convergence confirmed")
else:
    print("\nFAIL: ratios are not ~16 -> there is a bug in the RK4 code")

# On a log-log plot a 4th-order method is a straight line of slope 4.
plt.loglog(steps, errors, "o-", label="RK4 measured error")
ref = [errors[0] * (h / steps[0]) ** 4 for h in steps]
plt.loglog(steps, ref, "--", label="slope 4 (theory)")
plt.xlabel("step size h (s)")
plt.ylabel("max error in position")
plt.title("RK4 convergence on a mass-spring system")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.savefig("rk4_convergence.png", dpi=150, bbox_inches="tight")
print("Saved plot: rk4_convergence.png")