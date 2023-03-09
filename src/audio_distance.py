import spectogram
import numpy as np
import constants


def song_distance(audio, reference, sr_audio, sr_ref, min_freq, max_freq):
    # this function should calculate the similarity between two songs
    # the songs are both numpy arrays
    # you can use the functions above to help you
    # return the similarity
    mel_spectogram_audio = spectogram.create_mel_spectogram(audio, sr_audio, min_freq, max_freq)
    mel_spectogram_ref = spectogram.create_mel_spectogram(reference, sr_ref, min_freq, max_freq)

    power_audio = spectogram.create_power_spectogram(mel_spectogram_audio, constants.LOOKBACK)
    power_ref = spectogram.create_power_spectogram(mel_spectogram_ref, constants.LOOKBACK)

    distance = euclidean_distance(power_ref, power_audio)
    return distance


def euclidean_distance(a, b):
    # this function should calculate the euclidean distance between two average spectogram vectors
    # a and b are both numpy arrays
    return np.linalg.norm(a-b)


def manhattan_distance(a, b):
    # this function should calculate the manhattan distance between two average spectogram vectors
    # a and b are both numpy arrays
    return np.sum(np.abs(a-b))


def cosine_distance(a, b):
    # this function should calculate the cosine distance between two average spectogram vectors
    # a and b are both numpy arrays
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def moving_average(vector, lookback):
    # this function should calculate the moving average of a vector
    # the lookback is the number of samples to look back
    # the output should be the same size as the input
    # the first lookback samples should be the same as the input
    # the last lookback samples should be the same as the input
    return np.convolve(vector, np.ones(lookback)/lookback, mode='same')

if __name__ == "__main__":
    weight = np.exp(-np.arange(0, 128, 1) / 100)
    print(weight)



