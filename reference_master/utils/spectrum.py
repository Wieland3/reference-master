"""
File contains code for creating Power Spectrograms from audio files
"""

import librosa
import numpy as np
from reference_master import constants


def create_spectrum(audio, sr):
    """
    Creates a power cqt spectrogram from an audio file
    :param audio: audio file
    :param sr: sample rate of audio
    :return: Tuple of power spectrogram and frequencies
    """
    # Make sure that when the optimization changes the audio to NaN or Inf it is handled
    if np.isnan(audio).any() or np.isinf(audio).any() or np.isneginf(audio).any():
        zeros = np.zeros(len(audio))
        audio = zeros

    # Create the spectrogram
    spectrum = librosa.cqt(audio, sr = sr, fmin=constants.HP_FREQ, n_bins=120, hop_length=512, bins_per_octave=12)
    abs = np.abs(spectrum)

    # Average over the time axis and convert to dB
    power_mean = np.mean(abs **2, axis=1)
    power_d_b = librosa.power_to_db(power_mean)

    # Smooth the spectrum and return it
    smoothed = running_mean(power_d_b, constants.LOOKBACK)
    freqs = librosa.cqt_frequencies(n_bins=120, fmin=constants.HP_FREQ, bins_per_octave=12)
    return smoothed, freqs[constants.LOOKBACK - 1:]


def running_mean(x, N):
    """
    Smooths a vector by taking the mean over a window of size N
    :param x: Vector to smooth
    :param N: Window size
    :return:
    """
    return np.convolve(x, np.ones(N)/N, mode='valid')
