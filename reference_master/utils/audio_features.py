import numpy as np
import librosa


def crest_factor(audio):
    """
    calculates the crest factor of an audio signal
    :param audio: audio to operate on
    :return: crest factor of audio
    """
    max_signal = np.max(audio)
    return max_signal / rms(audio)


def rms(audio):
    """
    calculates the rms of an audio signal
    :param audio: audio to operate on
    :return: rms of audio
    """
    return np.sqrt(np.mean(np.square(audio)))


def tempo(audio, sr):
    """
    calculates the tempo of an audio signal
    :param audio: audio to operate on
    :return: tempo of audio
    """
    return librosa.beat.beat_track(y=audio, sr=sr)


def melody(audio, sr):
    """
    calculates the melody of an audio signal
    :param audio: audio to operate on
    :return: melody of audio
    """
    return librosa.feature.mfcc(y=audio, sr=sr)


def chroma(audio, sr):
    """
    calculates the chroma of an audio signal
    :param audio: audio to operate on
    :return: chroma of audio
    """
    return librosa.feature.chroma_cqt(y=audio, sr=sr)


def spectral_centroid(audio, sr):
    """
    calculates the spectral centroid of an audio signal
    :param audio: audio to operate on
    :return: spectral centroid of audio
    """
    return librosa.feature.spectral_centroid(y=audio, sr=sr)


def dynamic_range(audio):
    """
    calculates the dynamic range of an audio signal
    :param audio: audio to operate on
    :return: dynamic range of audio
    """
    return np.max(audio) - np.min(audio)


