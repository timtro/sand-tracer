import numpy as np


# yapf: disable
def phase_portrait(ax=None, f=lambda x, t: np.array([x[1], -x[0]]),
                   xrng=[-1, 1], yrng=[-1, 1], cmap='jet',
                   samples=31, arrow_width=0.0022, unit_arrows=False):
    # yapf: enable
    xwidth = xrng[1] - xrng[0]
    ywidth = yrng[1] - yrng[0]

    # Positions of arrow centres:
    X, Y = np.meshgrid(
        np.linspace(xrng[0] - .1 * xwidth, xrng[1] + .1 * xwidth, samples),
        np.linspace(yrng[0] - .1 * ywidth, yrng[1] + .1 * ywidth, samples))

    # Vectors in field
    u, v = f([X, Y], 0.)

    # Magnitude for colouring
    m = np.hypot(u, v)

    if unit_arrows:
        # Scale all arrows to unit length so only colour encodes magnitudes:
        for x, y in zip(u, v):
            h = np.hypot(x, y)
            x /= h
            y /= h

    # yapf: disable
    return ax.quiver(X, Y, u, v, m, pivot='mid', width=arrow_width,
                     scale=samples * 2, scale_units='height',
                     cmap=cmap)
