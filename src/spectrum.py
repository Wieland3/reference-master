import librosa
import numpy as np
import audio_utils
import matplotlib.pyplot as plt
import loudness
import audio_distance
import constants


def create_spectrum(audio, sr, n_fft=2048, hop_length=512):
    spectrum = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length)
    abs = np.abs(spectrum)
    power_mean = np.mean(abs ** 2, axis=1)
    power_dB = librosa.power_to_db(power_mean)
    #smoothed = audio_distance.moving_average(power_dB, constants.LOOKBACK)
    freqs = np.arange(0, 1 + n_fft / 2) * sr / n_fft
    return power_dB, freqs


if __name__ == '__main__':
    duration = 2
    raw, sr_raw = audio_utils.load_audio_file('../tracks/raw_tracks/2.wav')
    print("raw sr", sr_raw)
    raw_mono, raw_max = audio_utils.preprocess_audio(raw, sr_raw, duration)
    raw_loudness = loudness.get_loudness(raw_max, sr_raw)
    print("raw loudness", raw_loudness)

    ref, sr_ref = audio_utils.load_audio_file('../tracks/reference_tracks/BreakTheFall.mp3')
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
