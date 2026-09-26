import numpy as np

def rk4_step(f, t, y, h):
    """f(t, y) -> dy/dt."""
    k1 = f(t, y)
    k2 = f(t + h / 2, y + h * k1 / 2)
    k3 = f(t + h / 2, y + h * k2 / 2)
    k4 = f(t + h, y + h * k3)
    return y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

def rk4_integrate(f, t0, y0, h, n_steps):
    """Take n_steps RK4 steps of size h. Returns (times, states)."""
    y0 = np.atleast_1d(np.asarray(y0, dtype=float))
    t = np.empty(n_steps + 1)
    y = np.empty((n_steps + 1, y0.size))
    t[0], y[0] = t0, y0
    for i in range(n_steps):
        y[i + 1] = rk4_step(f, t[i], y[i], h)
        t[i + 1] = t[i] + h
    return t, y