import numpy as np

import audio_distance
from scipy.optimize import dual_annealing, differential_evolution, minimize


def objective(params, plugin, raw, reference, sr_raw, sr_ref):
    plugin.set_params(params)
    audio = plugin.process(raw, sr_raw)
    if np.isnan(audio).any() or np.isinf(audio).any() or np.isneginf(audio).any():
        print(params)
        plugin.show_editor()
    distance = audio_distance.song_distance(audio, reference, sr_raw, sr_ref)
    print(distance)
    return distance


def dual_annealing_optimization(plugin, bounds, raw, reference, sr_raw, sr_ref, maxiter):
    args = (plugin, raw, reference, sr_raw, sr_ref)
    return dual_annealing(func=objective, bounds=bounds, args=args, maxiter=maxiter)


