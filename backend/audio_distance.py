import numpy as np
import constants
from sklearn.preprocessing import MinMaxScaler
import spectrum


def song_distance(audio, sr_audio, power_ref):
    # this function should calculate the similarity between two songs
    # the songs are both numpy arrays
    # you can use the functions above to help you
    # return the similarity
    power_audio, power_freq = spectrum.create_spectrum(audio, sr_audio)
    power_ref, ref_freq = power_ref
    low_audio = power_audio[power_freq < 250]
    low_ref = power_ref[ref_freq < 250]
    low_distance = euclidean_distance(low_ref, low_audio)
    mid_audio = power_audio[(power_freq > 250) & (power_freq < 7500)]
    mid_ref = power_ref[(ref_freq > 250) & (ref_freq < 7500)]
    mid_distance = euclidean_distance(mid_ref, mid_audio)
    high_audio = power_audio[power_freq > 7500]
    high_ref = power_ref[ref_freq > 7500]
    high_distance = euclidean_distance(high_ref, high_audio)
    return low_distance + mid_distance + high_distance
    return low_distance * 4 + mid_distance * 0.13 + high_distance * 0.11


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



