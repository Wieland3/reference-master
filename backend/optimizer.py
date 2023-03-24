import numpy as np
import audio_distance
from scipy.optimize import dual_annealing


def objective(params, plugin, raw, sr_raw, power_ref):
    plugin.set_params(params)
    audio = plugin.process(raw, sr_raw)
    distance = audio_distance.song_distance(audio, sr_raw, power_ref)
    print(distance)
    return distance


def dual_annealing_optimization(plugin, bounds, raw, sr_raw, power_ref, maxiter):
    args = (plugin, raw, sr_raw, power_ref)
    return dual_annealing(func=objective, bounds=bounds, args=args, maxiter=maxiter)


