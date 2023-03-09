import audio_distance
from scipy.optimize import dual_annealing


def objective(params, plugin, raw, reference, sr_raw, sr_ref, min_freq, max_freq):
    plugin.set_params(params)
    audio = plugin.process(raw, sr_raw)
    distance = audio_distance.song_distance(audio, reference, sr_raw, sr_ref, min_freq, max_freq)
    print(distance)
    return distance


def dual_annealing_optimization(plugin, bounds, raw, reference, sr_raw, sr_ref, min_freq, max_freq, maxiter):
    args = (plugin, raw, reference, sr_raw, sr_ref, min_freq, max_freq)
    return dual_annealing(func=objective, bounds=bounds, args=args, maxiter=maxiter)


