# Author: Timothy A. V. Teatro
# Copyright 2017 by Timothy A. V. Teatro. All rights reserved.
# See LICENSE for details on GPL v3.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from pendulum_sim import PendulumState2D

from presets import presets

# initial_contidionts = dict(r=[.78, .9], b=0.04, xx0=[1, -.2], xy0=[-.33, .1])
initial_contidionts = presets['my2017']

# initial_contidionts = presets['a']


def pendulum_sim_generator():
    """ A generator which steps the simulation and returns the simulated state.
    """
    state = PendulumState2D(**initial_contidionts, dt=0.03)

    while True:
        yield state
        state.step()


if __name__ == '__main__':
    # Everything to do with plotting and animating.

    fig = plt.figure()
    ax = fig.add_subplot(
        111, aspect='equal', autoscale_on=False, xlim=(-1, 1), ylim=(-1, 1))
    fig.subplots_adjust(
        left=0.05, right=0.98, bottom=0.05, top=0.98, wspace=0.1)

    line, = ax.plot([], [], 'r-', lw=1)
    pith, = ax.plot([], [], 'o-', ms=15)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    energy_text = ax.text(0.02, 0.92, '', transform=ax.transAxes)

    XHistory = []
    YHistory = []

    def animate(sim_state):

        if np.abs(sim_state.energy()) <= 0.05 * sim_state.E0:
            sim_state.reset()
            XHistory.clear()
            YHistory.clear()
            return line, pith, time_text, energy_text

        XHistory.append(sim_state.xx[0])
        YHistory.append(sim_state.xy[0])
        pith.set_data(sim_state.xx[0], sim_state.xy[0])
        line.set_data(XHistory, YHistory)
        time_text.set_text('time = %.1f' % sim_state.t)
        energy_text.set_text('energy = %.2f J' % sim_state.energy())
        return line, pith, time_text, energy_text

    ani = animation.FuncAnimation(
        fig, animate, pendulum_sim_generator, blit=True, interval=10)
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()
