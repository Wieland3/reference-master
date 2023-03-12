import numpy as np
import constants
from sklearn.preprocessing import MinMaxScaler
import spectrum


def song_distance(audio, reference, sr_audio, sr_ref):
    # this function should calculate the similarity between two songs
    # the songs are both numpy arrays
    # you can use the functions above to help you
    # return the similarity
    power_audio, _ = spectrum.create_spectrum(audio, sr_audio)
    power_ref, _ = spectrum.create_spectrum(reference, sr_ref)
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


if __name__ == "__main__":
    weight = np.exp(-np.arange(0, 128, 1) / 100)
    print(weight)



