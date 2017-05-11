import numpy as np


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
        return np.array([x[1], -9.8 * np.sin(x[0]) / self.r - self.b * x[1]])

    def energy(s, x):
        T = s.m * (s.r * x[1])**2 / 2.
        U = -s.m * s.g * s.r * np.cos(x[0])
        return T + U

    def proj_horiz(self, pX):
        """ The dynamics are performed on the angular coordinates. For plotting,
            we'll want to convert with some basic trigonometry.
                x = r * sin(theta)
                dx/dt = r * cos(theta) * d.theta/dt
        """
        return np.array(
            [self.r * np.sin(pX[0]), self.r * np.cos(pX[0]) * pX[1]])


class PendulumSimulator2D:
    """ The class aggregates dynamics for two 1D pendulums which is isomorphic
        do a single 2D pendulum. (The x-direction doesn't care what the
        y-direction is doing, so the 2D problem is trivially decoupled into
        two 1D problems.)
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
        self.xx = np.array(xx0)
        self.xy = np.array(xy0)
        self.E0 = self.energy(xx0, xy0)  # Starting energy
        self.Erest = self.energy([0, 0], [0, 0])  # Rest energy
    # yapf: enable

    def energy(self, xx, xy):
        return self.px.energy(xx) + self.py.energy(xy)

    def __iter__(self):
        return self
