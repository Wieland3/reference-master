import numpy as np
from reference_master.utils import spectrum


def song_distance(audio, sr_audio, power_ref):
    """
    calculates the mse distance in the frequency domain between the audio and the reference
    :param audio: raw audio
    :param sr_audio: sample rate of raw audio
    :param power_ref: power spectrum of reference audio
    :return: distance between audio and reference
    """
    power_audio, power_freq = spectrum.create_spectrum(audio, sr_audio)
    distance = mse(power_ref, power_audio)
    return distance


def mse(a, b):
    """
    calculates the mean squared error between two vectors
    :param a: first vector
    :param b: second vector
    :return: mean squared error
    """
    return np.mean((a - b) ** 2)
