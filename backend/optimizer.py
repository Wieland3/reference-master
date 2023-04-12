import sys
sys.path.append('../')
import numpy as np
from scipy.optimize import dual_annealing, differential_evolution, direct
from backend import audio_distance


def objective(params, plugin, raw, sr_raw, power_ref):
    plugin.set_params(params)
    audio = plugin.process(raw, sr_raw)
    distance = audio_distance.song_distance(audio, sr_raw, power_ref)
    print(distance)
    return distance


def dual_annealing_optimization(plugin, bounds, raw, sr_raw, power_ref, maxiter):
    args = (plugin, raw, sr_raw, power_ref)
    x0 = np.array([0.0, 1, 100, 0.0, 1, 1000, 0.0, 1, 5000, 0.0, 1, 7500])
    return dual_annealing(func=objective, bounds=bounds, args=args, maxiter=maxiter, x0=x0)


def direct_optimization(plugin, bounds, raw, sr_raw, power_ref, maxiter):
    args = (plugin, raw, sr_raw, power_ref)
    return direct(func=objective, bounds=bounds, args=args, maxiter=maxiter, f_min=0.0)



