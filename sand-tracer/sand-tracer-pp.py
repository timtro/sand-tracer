# Author: Timothy A. V. Teatro
# Copyright 2017 by Timothy A. V. Teatro. All rights reserved.
# See LICENSE for details on GPL v3.

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

from pendulum_sim import PendulumSimulator2D, presets
from plot_helpers import phase_portrait


class PendulumSimulatorIterator(PendulumSimulator2D):

    def __next__(self):
        # Will return current data, and tee-up for next iteration.
        prevX = (self.t, self.px.proj_horiz(self.xx),
                 self.py.proj_horiz(self.xy),
                 self.energy(self.xx, self.xy) - self.Erest)

        self.xx = integrate.odeint(self.px.dxdt, self.xx, [0, self.dt])[-1]
        self.xy = integrate.odeint(self.py.dxdt, self.xy, [0, self.dt])[-1]
        self.t += self.dt
        return prevX


if __name__ == '__main__':
    # Everything to do with plotting and animating.
    sim = PendulumSimulatorIterator(**presets[0], dt=0.07)

    fig, axs = plt.subplots(1, 2)

    axs[0].set(aspect='equal', autoscale_on=False, xlim=(-1, 1), ylim=(-1, 1))
    axs[1].set(aspect=0.5, autoscale_on=False, xlim=(-1, 1), ylim=(-2, 2))
    fig.subplots_adjust(
        left=0.05, right=0.98, bottom=0.05, top=0.98, wspace=0.1)

    line, = axs[0].plot([], [], 'r-', lw=1)
    pith, = axs[0].plot([], [], 'o-', ms=15)
    time_text = axs[0].text(0.02, 0.95, '', transform=axs[0].transAxes)

    phase_portrait(
        axs[1],
        sim.px.dxdt,
        samples=51,
        xlim=[-1, 1],
        ylim=[-2, 2],
        cmap='viridis')

    pline, = axs[1].plot([], [], 'b-', lw=1)
    ppoint, = axs[1].plot([], [], 'o-', ms=15)
    energy_text = axs[1].text(0.02, 0.95, '', transform=axs[1].transAxes)

    XHistory = []
    YHistory = []
    WHistory = []

    def animate(data):
        """ Here, the type of 'data' is the return from the iterator
                PendulumSimulatorIterator.__next__()
        """
        t, X, Y, E = data
        XHistory.append(X[0])
        YHistory.append(Y[0])
        WHistory.append(X[1])

        pith.set_data(X[0], Y[0])
        line.set_data(XHistory, YHistory)
        time_text.set_text('time = %.1f s' % t)

        ppoint.set_data(X[0], X[1])
        pline.set_data(XHistory, WHistory)
        energy_text.set_text('energy = %.2f J' % E)

        return line, pith, time_text, ppoint, pline, energy_text

    ani = animation.FuncAnimation(fig, animate, sim, blit=True, interval=0)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()
