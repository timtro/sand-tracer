# Author: Timothy A. V. Teatro
# Copyright 2017 by Timothy A. V. Teatro. All rights reserved.
# See LICENSE for details on GPL v3.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.integrate as integrate

from pendulum_sim import PendulumSimulator2D


class PendulumSimulatorIterator(PendulumSimulator2D):

    def __next__(self):
        # Will return current data, and tee-up for next iteration.
        prevX = (self.t, self.angular_to_cartesian(self.xx),
                 self.angular_to_cartesian(self.xy))
        self.xx = integrate.odeint(self.px.dxdt, self.xx, [0, self.dt])[-1]
        self.xy = integrate.odeint(self.py.dxdt, self.xy, [0, self.dt])[-1]
        self.t += self.dt
        return prevX


if __name__ == '__main__':
    # Everything to do with plotting and animating.
    preset = []
    preset.append(dict(r=[2, 1.4], b=0.01))
    preset.append(dict(r=[2, 1.8], b=0.02))
    sim = PendulumSimulatorIterator(**preset[1], dt=0.03)

    fig = plt.figure()
    ax = fig.add_subplot(
        111, aspect='equal', autoscale_on=False, xlim=(-1, 1), ylim=(-1, 1))
    fig.subplots_adjust(
        left=0.05, right=0.98, bottom=0.05, top=0.98, wspace=0.1)

    line, = ax.plot([], [], 'r-', lw=1)
    pith, = ax.plot([], [], 'o-', ms=15)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    XHistory = []
    YHistory = []

    def animate(data):
        """ Here, the type of 'data' is the return from the iterator
                PendulumSimulatorIterator.__next__()
        """
        t, X, Y = data
        XHistory.append(X[0])
        YHistory.append(Y[0])
        pith.set_data(X[0], Y[0])
        line.set_data(XHistory, YHistory)
        time_text.set_text('time = %.1f' % t)
        return line, pith, time_text

    ani = animation.FuncAnimation(fig, animate, sim, blit=True, interval=0)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()
