from scipy.optimize import dual_annealing, direct
from mastering.utils import audio_distance

def objective(params, plugin, raw, sr_raw, power_ref):
    plugin.set_params(params)
    audio = plugin.process(raw, sr_raw)
    distance = audio_distance.song_distance(audio, sr_raw, power_ref)
    print(distance)
    return distance


def dual_annealing_optimization(plugin, bounds, raw, sr_raw, power_ref, maxiter):
    args = (plugin, raw, sr_raw, power_ref)

    #center_freq_x0 = [60, 125, 300, 1500, 1700, 2500, 2700, 3500, 3700, 4200, 6000, 10000]
    #gain_x0 = [0 for _ in range(12)]
    #q_x0 = [1 for _ in range(12)]
    #x0 = np.array(gain_x0 + center_freq_x0 + q_x0)
    return dual_annealing(func=objective, bounds=bounds, args=args, maxiter=maxiter)


def direct_optimization(plugin, bounds, raw, sr_raw, power_ref, maxiter):
    args = (plugin, raw, sr_raw, power_ref)
    return direct(func=objective, bounds=bounds, args=args, maxiter=maxiter, f_min=0.0)



