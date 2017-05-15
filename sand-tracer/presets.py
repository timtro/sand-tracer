import numpy as np

presets = dict()
presets['my2017'] = dict(
    r=[np.sqrt(2) / 2, 1], b=0.03, xx0=[.9, 0], xy0=[-.9, 0])
presets['a'] = dict(r=[2, 1.4], b=0.01)
presets['b'] = dict(r=[2, 1.8], b=0.02)
presets['c'] = dict(r=[.8, .9], b=0.02)
presets['d'] = dict(r=[1, 1], b=0.02, xx0=[.25, 0], xy0=[0, -.9])
