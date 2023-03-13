import librosa
import numpy as np
import audio_utils
import matplotlib.pyplot as plt
import loudness
import audio_distance
import constants


def create_spectrum(audio, sr, n_fft=8192, hop_length=2048):
    if np.isnan(audio).any() or np.isinf(audio).any() or np.isneginf(audio).any():
        zeros = np.zeros(len(audio))
        audio = zeros
    spectrum = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length)
    abs = np.abs(spectrum)
    power_mean = np.mean(abs ** 2, axis=1)
    power_dB = librosa.power_to_db(power_mean)
    smoothed = running_mean(power_dB, constants.LOOKBACK)
    freqs = running_mean(np.arange(0, 1 + n_fft / 2) * sr / n_fft, constants.LOOKBACK)
    smoothed = smoothed[freqs < 17000]
    freqs = freqs[freqs < 17000]
    return smoothed, freqs


def running_mean(x, N):
    return np.convolve(x, np.ones(N)/N, mode='valid')


if __name__ == '__main__':
    duration = 2
    raw, sr_raw = audio_utils.load_audio_file('../tracks/raw_tracks/5.wav')
    print("raw sr", sr_raw)
    raw_mono, raw_max = audio_utils.preprocess_audio(raw, sr_raw, duration)
    raw_loudness = loudness.get_loudness(raw_max, sr_raw)
    print("raw loudness", raw_loudness)

    ref, sr_ref = audio_utils.load_audio_file('../tracks/reference_tracks/LoseYourself.mp3')
    print("ref sr", sr_ref)
    ref_mono, ref_max = audio_utils.preprocess_audio(ref, sr_ref, duration)
    ref_loudness = loudness.get_loudness(ref_max, sr_ref)
    ref_loudness_adjusted = loudness.equal_loudness(ref_max, sr_ref, raw_loudness)
    ref_mono = audio_utils.preprocess_audio(ref_loudness_adjusted, sr_ref, None)[0]

    raw_spectrum, raw_freqs = create_spectrum(raw_mono, sr_raw)
    ref_spectrum, ref_freqs = create_spectrum(ref_mono, sr_ref)
    plt.plot(raw_freqs, raw_spectrum, label='raw')
    plt.plot(ref_freqs, ref_spectrum, label='reference')
    plt.legend(loc="lower left")
    plt.show()
