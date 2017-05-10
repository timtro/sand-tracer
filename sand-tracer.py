# Author: Timothy A. V. Teatro
# Copyright 2017 by Timothy A. V. Teatro. All rights reserved.
# See LICENSE for details on GPL v3.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.integrate as integrate


class Pendulum1D:
    """ Just the dynamics of the pendulum. Constants related to pendulum
        design:
                # Radius: r
                # Pith pass: m
                # Drag loss coefficient: b
                # Acceleration due to gravity: g
        are stored here, but not the pendulum's state.
    """

    def __init__(self, r=1, m=.5, b=.2, g=9.807):

        self.r = r
        self.m = m
        self.b = b
        self.g = g

    def dxdt(self, x, t):
        # State of pendulum: x ∈ R^2, contains angular position and speed.
        return np.array([x[1], -9.8 * np.sin(x[0]) / self.r - self.b * x[1]])

    def energy(self, x):
        T = self.m * self.r**2 * x[1]**2 / 2
        U = -self.m * self.g * self.r * np.cos(x[0])
        return T + U


class PendulumSimulator2D:
    """ The class aggregates dynamics for two 1D pendulums which is isomorphic
        do a single 2D pendulum. (The x-direction doesn't care what the
        y-direction is doing, so the 2D problem is trivially decoupled into
        two 1D problems.)
    """

    def __init__(self, r=[1, 1], m=0.5, b=0.2, g=9.807, dt=0.1):
        self.dt = dt
        self.px = Pendulum1D(r=r[0], m=m, b=b, g=g)
        self.py = Pendulum1D(r=r[1], m=m, b=b, g=g)

        # Initial conditions
        self.t = 0
        self.xx = np.array([0, -1])
        self.xy = np.array([0, 1])

    def angular_pos_vel_to_cartesian(self, pX):
        """ The dynamics are performed on the angular coordinates. For plotting,
            we'll want to convert with some basic trigonometry.
                x = r * sin(theta)
                dx/dt = r * cos(theta) * d.theta/dt
        """
        return np.array(
            [self.px.r * np.sin(pX[0]), self.py.r * np.cos(pX[0]) * pX[1]])

    def __iter__(self):
        return self

    def __next__(self):
        prevX = (self.t, self.angular_pos_vel_to_cartesian(self.xx),
                 self.angular_pos_vel_to_cartesian(self.xy))
        self.xx = integrate.odeint(self.px.dxdt, self.xx, [0, self.dt])[-1]
        self.xy = integrate.odeint(self.py.dxdt, self.xy, [0, self.dt])[-1]
        self.t += self.dt
        return prevX


if __name__ == '__main__':
    # Everything to do with plotting and animating.
    preset = []
    preset.append(dict(r=[2, 1.4], b=0.01))
    preset.append(dict(r=[2, 1.8], b=0.03))
    sim = PendulumSimulator2D(**preset[0])

    fig = plt.figure()
    ax = fig.add_subplot(
        111, aspect='equal', autoscale_on=False, xlim=(-1, 1), ylim=(-1, 1))

    pith, = ax.plot([], [], 'o-', ms=15)
    line, = ax.plot([], [], 'r-', lw=1)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    XHist = []
    YHist = []

    def init():
        pith.set_data([], [])
        line.set_data([], [])
        time_text.set_text('')
        return pith, line, time_text

    def animate(data):
        t, X, Y = data
        XHist.append(X[0])
        YHist.append(Y[0])
        pith.set_data(X[0], Y[0])
        line.set_data(XHist, YHist)
        time_text.set_text('time = %.1f' % t)
        return pith, line, time_text

    ani = animation.FuncAnimation(
        fig,
        animate,
        sim,
        blit=False,
        interval=1,
        repeat=False,
        init_func=init)
    plt.show()
