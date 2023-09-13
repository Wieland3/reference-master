"""
File for calculating and normalizing loudness of audio signals
"""


import pyloudnorm


def get_loudness(audio, sr):
    """
    calculates the loudness of an audio signal
    :param audio: audio to operate on
    :param sr: sample rate of audio
    :return: loudness of audio
    """
    meter = pyloudnorm.Meter(sr)
    loudness = meter.integrated_loudness(audio)
    return loudness


def equal_loudness(audio, sr, target_loudness):
    """
    normalizes the loudness of an audio signal to a target loudness
    :param audio: audio to operate on
    :param sr: sample rate of audio
    :param target_loudness: loudness to normalize to
    :return: audio with loudness equal to target_loudness
    """
    meter = pyloudnorm.Meter(sr)
    loudness = meter.integrated_loudness(audio)
    audio = pyloudnorm.normalize.loudness(audio, loudness, target_loudness)
    return audio
