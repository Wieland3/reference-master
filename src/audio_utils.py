import librosa
import soundfile as sf
import numpy as np
import loudness


def load_audio_file(file_path):
    # this function should load an wav audio file  with librosa and remain the same sample rate as the original file
    audio, sr = sf.read(file_path)
    return audio, sr


def find_chorus(audio, sr, window_length):
    loudest_i = 0
    loudest = -100000
    for i in range(0, audio.shape[0], window_length):
        current_audio = audio[i:i + window_length]
        if current_audio.shape[0] != window_length:
            continue
        current_loudness = loudness.get_loudness(current_audio, sr)
        if current_loudness > loudest:
            loudest = current_loudness
            loudest_i = i
    return audio[loudest_i:loudest_i + window_length]


def select_max_audio(audio, sr, length):
    # function to select the location of the amplitude and returns length seconds around this location
    max_amp = np.argmax(audio, axis=0)[0]
    start = max_amp - (sr * length)
    end = max_amp + (sr * length)
    return audio[start:end, :]


def preprocess_audio(audio, sr, duration=None):
    # function to preprocess the audio
    # this function should be called before the audio is passed to the optimizer
    # this function should return the preprocessed audi and the sample rate of the audio
    if duration is not None:
        max = find_chorus(audio, sr, sr * duration)
    else:
        max = audio
    #reshaped = max.reshape(2, -1)
    mono = np.sum(max, axis=1)
    return mono, max


def numpy_to_wav(audio, sr, file_path):
    # function to save a numpy array as a wav file with soundfile
    sf.write(file_path, audio, sr)



