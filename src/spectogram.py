import librosa
import numpy as np
import matplotlib.pyplot as plt
import audio_utils
import audio_distance
import constants


def create_mel_spectogram(audio, sr, min_freq, max_freq, n_fft=2048 ,n_mels=constants.N_MELS):
    # this function should create a chroma stf from an audio file
    #spec = np.abs(librosa.stft(audio, n_fft=n_fft, win_length=n_fft//2, hop_length=n_fft//4))
    spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=n_fft, n_mels=n_mels, fmin=min_freq, fmax=max_freq)
    spec = librosa.util.normalize(spec)
    return spec


def create_power_spectogram(mel_spectogram, lookback=None):
    if lookback is not None:
        power = np.log(audio_distance.moving_average(np.average(mel_spectogram, axis=1), lookback) + 1e-8)
    else:
        power = np.log(np.average(mel_spectogram, axis=1) + 1e-8)
    return power


def plot_mel_spectogram(mel_spectogram):
    # this function should plot the mel spectogram
    plt.figure(figsize=(10, 4))  # set the size of the figure
    librosa.display.specshow(mel_spectogram, y_axis='mel', fmax=20000, x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel spectrogram')
    plt.tight_layout()
    plt.show()


def plot_power_spectogram(raw, reference, processed=None, dif_before = None, dif_after = None):
    # this function should plot the power spectogram in logarithmic scale
    plt.figure(figsize=(10, 4))  # set the size of the figure
    plt.plot(raw, label='raw')
    plt.plot(reference, label='reference')
    if not processed is None:
        plt.plot(processed, label='processed')
    if not dif_before is None:
        plt.plot(dif_before, label='dif')
    if not dif_after is None:
        plt.plot(dif_after, label='dif_after')
        plt.axhline(y=0, color='k')

    #plt.yscale("log")
    plt.title('Power spectogram')
    plt.tight_layout()
    plt.legend(loc="lower left")
    plt.show()


if __name__ == '__main__':
    raw, sr = audio_utils.load_audio_file('../tracks/raw_tracks/0.wav')
    raw, raw_max = audio_utils.preprocess_audio(raw, sr, constants.DURATION)
    #ref, sr = audio_utils.load_audio_file('../tracks/edited/reference.wav')
    #ref, _ = audio_utils.preprocess_audio(ref, sr, constants.DURATION)
    #processed, sr = audio_utils.load_audio_file('../tracks/edited/processed.wav')
    #processed, _ = audio_utils.preprocess_audio(processed, sr, constants.DURATION)

    #mel_spectogram_raw = create_mel_spectogram(raw, sr, 0, 20000)
    #power_spectogram_raw = create_power_spectogram(mel_spectogram_raw,10)
    #print(power_spectogram_raw.min())
    #print(power_spectogram_raw.max())
    #mel_spectogram_ref = create_mel_spectogram(ref, sr, 0, 20000)
    #mel_spectogram_pro = create_mel_spectogram(processed, sr, 0, 20000)

    #lookback = constants.LOOKBACK



    find = 200
    freqs = librosa.core.mel_frequencies(fmin=0.0, fmax=20000, n_mels=constants.N_MELS)
    bin = np.argmin(abs(freqs - find))

    print(bin)
    '''
    average_raw = audio_distance.moving_average(np.average(mel_spectogram_raw, axis=1),lookback)
    average_ref = audio_distance.moving_average(np.average(mel_spectogram_ref, axis=1),lookback)
    average_pro = audio_distance.moving_average(np.average(mel_spectogram_pro, axis=1),lookback)

    average_raw = create_power_spectogram(mel_spectogram_raw, lookback)
    average_ref = create_power_spectogram(mel_spectogram_ref, lookback)
    average_pro = create_power_spectogram(mel_spectogram_pro, lookback)
    plot_power_spectogram(average_raw, average_ref, average_pro)
    '''