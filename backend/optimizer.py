import numpy as np
import audio_distance
from scipy.optimize import dual_annealing


def objective(params, plugin, raw, sr_raw, power_ref):
    plugin.set_params(params)
    audio = plugin.process(raw, sr_raw)
    if np.isnan(audio).any() or np.isinf(audio).any() or np.isneginf(audio).any():
        print(params)
        plugin.show_editor()
    distance = audio_distance.song_distance(audio, sr_raw, power_ref)
    print(distance)
    return distance


def dual_annealing_optimization(plugin, bounds, raw, sr_raw, power_ref, maxiter):
    args = (plugin, raw, sr_raw, power_ref)
    return dual_annealing(func=objective, bounds=bounds, args=args, maxiter=maxiter)


