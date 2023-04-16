import sys
sys.path.append('../')
import librosa
import numpy as np
from backend import constants


def create_spectrum(audio, sr):
    if np.isnan(audio).any() or np.isinf(audio).any() or np.isneginf(audio).any():
        zeros = np.zeros(len(audio))
        audio = zeros
    spectrum = librosa.cqt(audio, sr = sr, fmin=constants.HP_FREQ, n_bins=120, hop_length=512, bins_per_octave=12)
    abs = np.abs(spectrum)
    power_mean = np.mean(abs **2, axis=1)
    power_d_b = librosa.power_to_db(power_mean)
    smoothed = running_mean(power_d_b, constants.LOOKBACK)
    freqs = librosa.cqt_frequencies(n_bins=120, fmin=constants.HP_FREQ, bins_per_octave=12)
    return smoothed, freqs[constants.LOOKBACK - 1:]


def running_mean(x, N):
    return np.convolve(x, np.ones(N)/N, mode='valid')
