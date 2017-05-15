# Author: Timothy A. V. Teatro
# Copyright 2017 by Timothy A. V. Teatro. All rights reserved.
# See LICENSE for details on GPL v3.

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from pendulum_sim import PendulumState2D
from plot_helpers import phase_portrait
from presets import presets

# initial_contidionts = dict(r=[.78, .9], b=0.04, xx0=[1, -.2], xy0=[-.33, .1])
# initial_contidionts = presets['my2017']
initial_contidionts = presets['a']


def pendulum_sim_generator():
    """ A generator which steps the simulation and returns the simulated state.
    """
    state = PendulumState2D(**initial_contidionts, dt=0.03)

    while True:
        yield state
        state.step()


if __name__ == '__main__':
    # Everything to do with plotting and animating.

    fig, axs = plt.subplots(1, 2)

    axs[0].set(aspect='equal', autoscale_on=False, xlim=(-1, 1), ylim=(-1, 1))
    axs[1].set(aspect=0.5, autoscale_on=False, xlim=(-1, 1), ylim=(-2, 2))
    fig.subplots_adjust(
        left=0.05, right=0.98, bottom=0.05, top=0.98, wspace=0.1)

    line, = axs[0].plot([], [], 'r-', lw=1)
    pith, = axs[0].plot([], [], 'o-', ms=15)
    time_text = axs[0].text(0.02, 0.95, '', transform=axs[0].transAxes)

    # It is weird, but I pulled the first value out of the simulation generator
    # to get a reference to the state, so that I could access the dxdt member
    # to make the phase-portrait:
    phase_portrait(
        axs[1],
        next(pendulum_sim_generator()).px.dxdt,
        samples=51,
        xlim=[-1, 1],
        ylim=[-2, 2],
        cmap='jet')

    pline, = axs[1].plot([], [], 'b-', lw=1)
    ppoint, = axs[1].plot([], [], 'o-', ms=15)
    energy_text = axs[1].text(0.02, 0.95, '', transform=axs[1].transAxes)

    XHistory = []
    YHistory = []
    WHistory = []

    def animate(sim_state):
        """ Here, the type of 'data' is the return from the iterator
                PendulumSimulatorIterator.__next__()
        """

        if np.abs(sim_state.energy()) <= 0.05 * sim_state.E0:
            sim_state.reset()
            XHistory.clear()
            YHistory.clear()
            WHistory.clear()
            return line, pith, time_text, ppoint, pline, energy_text

        XHistory.append(sim_state.xx[0])
        YHistory.append(sim_state.xy[0])
        WHistory.append(sim_state.xx[1])

        pith.set_data(sim_state.xx[0], sim_state.xy[0])
        line.set_data(XHistory, YHistory)
        time_text.set_text('time = %.1f s' % sim_state.t)

        ppoint.set_data(sim_state.xx[0], sim_state.xx[1])
        pline.set_data(XHistory, WHistory)
        energy_text.set_text('energy = %.2f J' % sim_state.energy())

        return line, pith, time_text, ppoint, pline, energy_text

    ani = animation.FuncAnimation(
        fig, animate, pendulum_sim_generator, blit=True, interval=10)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()
