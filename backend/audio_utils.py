import soundfile as sf
import numpy as np
from backend import loudness


def load_audio_file(file_path):
    """
    loads an audio file
    :param file_path: path to audio file
    :return: tuple of audio and sample rate
    """
    audio, sr = sf.read(file_path)
    return audio, sr


def find_chorus(audio, sr, window_length):
    """
    finds the chorus of an audio file by finding the part with the highest integrated loudness
    :param audio: audio to find the chorus in
    :param sr: sample rate of audio
    :param window_length: is number of samples for the size of the window
    :return: audio cropped to the chorus
    """
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


def preprocess_audio(audio, sr, duration=None):
    """
    preprocesses an audio file by converting it to mono and finding the chorus
    if duration is None the whole audio is used and no chorus is selected
    :param audio: audio to operate on
    :param sr: sample rate of audio
    :param duration: length of the chorus in seconds
    :return: tuple of mono audio and stereo audio
    """
    if duration is not None:
        stereo = find_chorus(audio, sr, duration * sr)
    else:
        stereo = audio
    mono = np.sum(stereo, axis=1)
    return mono, stereo


def numpy_to_wav(audio, sr, file_path):
    """
    saves an audio file as a wav file
    :param audio: audio to operate on
    :param sr: sample rate of audio
    :param file_path: path to save the audio file to
    :return: None
    """
    sf.write(file_path, audio, sr)



