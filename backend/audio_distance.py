import sys
sys.path.append('../')
import numpy as np
from backend import spectrum


def song_distance(audio, sr_audio, power_ref):
    # this function should calculate the similarity between two songs
    # the songs are both numpy arrays
    # you can use the functions above to help you
    # return the similarity
    power_audio, power_freq = spectrum.create_spectrum(audio, sr_audio)
    power_ref, ref_freq = power_ref
    # Fit and transform minmax scaler to the power_ref and power_audio
    #data = np.concatenate((power_ref, power_audio))
    #scaler = MinMaxScaler()
    #scaler.fit(data.reshape(-1, 1))
    #power_ref = scaler.transform(power_ref.reshape(-1, 1)).reshape(-1)
    #power_audio = scaler.transform(power_audio.reshape(-1, 1)).reshape(-1)
    distance = mse(power_ref, power_audio)
    return distance

def mse(a, b):
    return np.mean((a - b) ** 2)

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



