import librosa
import numpy as np
from mastering import audio_features
from mastering import audio_utils


class FeatureEmbedding:
    def __init__(self, audio, sr):
        self.audio = audio
        self.sr = sr
        self.feature_vector = self.create_feature_vector()

    def create_feature_vector(self):
        # Tempo Features
        tempo, _ = audio_features.tempo(self.audio, self.sr)
        tempo = np.atleast_1d(tempo)

        # Melody Features
        melody = np.mean(audio_features.melody(self.audio, self.sr), axis=1)

        # Chroma Features
        chroma = np.mean(audio_features.chroma(self.audio, self.sr), axis=1)

        # Spectral Features
        spectral_centroid = audio_features.spectral_centroid(self.audio, self.sr)
        spectral_centroid_mean = np.atleast_1d(np.mean(spectral_centroid))
        spectral_centroid_std = np.atleast_1d(np.std(spectral_centroid))
        spectral_centroid_max = np.atleast_1d(np.max(spectral_centroid))
        spectral_centroid_min = np.atleast_1d(np.min(spectral_centroid))

        # Dynamic Features
        dynamic_range = np.atleast_1d(audio_features.dynamic_range(self.audio))
        return np.concatenate((melody, chroma, spectral_centroid_mean, spectral_centroid_std,
                               spectral_centroid_max, spectral_centroid_min, dynamic_range, tempo))

'''
audio, sr = audio_utils.load_audio_file("../tracks/raw_tracks/1.wav")
audio, _ = audio_utils.preprocess_audio(audio, sr, 10)
feature_embedding = FeatureEmbedding(audio, sr)
print(feature_embedding.feature_vector.shape)
print(feature_embedding.feature_vector)
'''