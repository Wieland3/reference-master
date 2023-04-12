import os
import sys
sys.path.append('../')
import soundfile as sf
import numpy as np
from backend import loudness



def load_audio_file(file_path):
    # this function should load an wav audio file  with librosa and remain the same sample rate as the original file
    audio, sr = sf.read(file_path)
    return audio, sr


def find_chorus(audio, sr, window_length):
    loudest_i = 0
    loudest = -100000
    for i in range(0, audio.shape[0], sr):
        current_audio = audio[i:i + window_length]
        if current_audio.shape[0] != window_length:
            continue
        current_loudness = loudness.get_loudness(current_audio, sr)
        if current_loudness > loudest:
            loudest = current_loudness
            loudest_i = i
    return audio[loudest_i:loudest_i + window_length]


def interaural_level_difference(audio):
    # function to calculate the interaural level difference of an audio signal
    # the audio signal is a numpy array
    # return the interaural level difference
    left = audio[:, 0]
    right = audio[:, 1]
    return np.mean(np.abs(left - right))


def crest_factor(audio):
    # function to calculate the crest factor of an audio signal
    # the audio signal is a numpy array
    # the sample rate is an integer
    # return the crest factor
    max = np.max(audio)
    return max / rms(audio)


def rms(audio):
    # function to calculate the root mean square of an audio signal
    # the audio signal is a numpy array
    # the sample rate is an integer
    # return the root mean square
    return np.sqrt(np.mean(np.square(audio)))


def preprocess_audio(audio, sr, duration=None):
    # function to preprocess the audio
    # this function should be called before the audio is passed to the optimizer
    # this function should return the preprocessed audi and the sample rate of the audio
    if duration is not None:
        max = find_chorus(audio, sr, duration * sr)
    else:
        max = audio
    #reshaped = max.reshape(2, -1)
    mono = np.sum(max, axis=1)
    return mono, max


def numpy_to_wav(audio, sr, file_path):
    # function to save a numpy array as a wav file with soundfile
    sf.write(file_path, audio, sr)



