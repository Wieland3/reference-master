import librosa
import numpy as np
import constants


def create_spectrum(audio, sr, n_fft=8192, hop_length=2048):
    if np.isnan(audio).any() or np.isinf(audio).any() or np.isneginf(audio).any():
        zeros = np.zeros(len(audio))
        audio = zeros
    spectrum = librosa.cqt(audio, sr = sr, fmin=constants.HP_FREQ, n_bins=120, hop_length=512, bins_per_octave=12)
    abs = np.abs(spectrum)
    power_mean = np.mean(abs **2, axis=1)
    power_dB = librosa.power_to_db(power_mean)
    smoothed = running_mean(power_dB, constants.LOOKBACK)
    #freqs = running_mean(np.arange(0, 1 + n_fft / 2) * sr / n_fft, constants.LOOKBACK)
    #smoothed = smoothed[freqs < 17000]
    #freqs = freqs[freqs < 17000]
    freqs = librosa.cqt_frequencies(n_bins=abs.shape[0], fmin=constants.HP_FREQ, bins_per_octave=24)
    return smoothed, freqs[constants.LOOKBACK - 1:]


def running_mean(x, N):
    return np.convolve(x, np.ones(N)/N, mode='valid')
