import numpy as np
from scipy.integrate import odeint


class Pendulum1D:
    """ Just the dynamics of the pendulum. Constants related to pendulum
        design are stored here, but not the pendulum's state.
    """

    def __init__(self, r=1, m=.5, b=.2, g=9.807):
        self.r = r  # Radius, or length of string.
        self.m = m  # Pith mass
        self.b = b  # Drag loss coefficient
        self.g = g  # Acceleration due to gravity

    def dxdt(self, x, t):
        # State of pendulum: x ∈ R^2, contains angular position and speed.
        return np.array(
            [x[1], -9.8 * np.sin(x[0]) / self.r - self.b * x[1] / self.m])

    def energy(s, x):
        T = s.m * (s.r * x[1])**2 / 2.
        U = s.m * s.g * s.r * (1 - np.cos(x[0]))
        return T + U

    def proj_horiz(self, pX):
        """ The dynamics are performed on the angular coordinates. For plotting,
            we'll want to convert with some basic trigonometry.
                x = r * sin(theta)
                dx/dt = r * cos(theta) * d.theta/dt
        """
        return np.array(
            [self.r * np.sin(pX[0]), self.r * np.cos(pX[0]) * pX[1]])


class PendulumState2D:
    """ The class aggregates dynamics for two 1D pendulums, simulating a 2D
        pendulum.
    """

    # yapf: disable
    def __init__(self, r=[1, 1], m=0.5, b=0.2, g=9.807, dt=0.1,  # As before
                 xx0=[0, 1],    # Initial state of x-pendulum
                 xy0=[0, -1]):  # Initial state of y-pendulum
        self.dt = dt
        self.px = Pendulum1D(r=r[0], m=m, b=b, g=g)
        self.py = Pendulum1D(r=r[1], m=m, b=b, g=g)

        # Initial conditions
        self.t = 0
        self.xx, self.xy = np.array(xx0), np.array(xy0)
        self.xx0, self.xy0 = np.array(xx0), np.array(xy0)
        self.E0 = self.energy(xx0, xy0)  # Starting energy
    # yapf: enable

    def reset(self):
        self.t = 0
        self.xx, self.xy = self.xx0, self.xy0

    def energy(self, xx=None, xy=None):
        if xx is None:
            xx, xy = self.xx, self.xy
        return self.px.energy(xx) + self.py.energy(xy)

    def step(self):
        self.xx = odeint(self.px.dxdt, self.xx, [0, self.dt])[-1]
        self.xy = odeint(self.py.dxdt, self.xy, [0, self.dt])[-1]
        self.t += self.dt
