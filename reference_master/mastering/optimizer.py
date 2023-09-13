"""
File contains code for optimizing the parameters of a plugin
"""

from scipy.optimize import dual_annealing
from reference_master.utils import audio_distance

def objective(params, plugin, raw, sr_raw, power_ref):
    """
    Objective function for the optimization
    :param params: parameters of the plugin
    :param plugin: plugin to process with
    :param raw: raw track to process
    :param sr_raw: sample rate of raw track
    :param power_ref: power spectrum of reference track
    :return: audio distance between processed track and reference track
    """
    plugin.set_params(params)
    audio = plugin.process(raw, sr_raw)
    distance = audio_distance.song_distance(audio, sr_raw, power_ref)
    print(distance)
    return distance


def dual_annealing_optimization(plugin, bounds, raw, sr_raw, power_ref, maxiter):
    """
    Performs a dual annealing optimization on the plugin
    :param plugin: Plugin to use
    :param bounds: Lower and Upper Bounds for the params
    :param raw: Raw Track to process
    :param sr_raw: Sample Rate of the Raw Track
    :param power_ref: Power Spectrum of the Reference Track
    :param maxiter: Maximum number of iterations
    :return:
    """
    args = (plugin, raw, sr_raw, power_ref)
    return dual_annealing(func=objective, bounds=bounds, args=args, maxiter=maxiter)
