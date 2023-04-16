import numpy as np
import librosa
from backend import audio_utils
from backend import loudness


class CustomClipper():

    def __init__(self):
        self.threshold = 10 ** (-1.2 / 20)
        self.gain = 0
        self.fade_in_duration = 0.1

    def set_params(self, values):
        self.gain = values[0]

    def process(self, audio, sr):
        fade_in_samples = int(self.fade_in_duration * sr)
        zero_crossings = np.nonzero(np.diff(np.sign(audio[:, 0])) + np.diff(np.sign(audio[:, 1])))[0]
        first_zero_crossing = zero_crossings[0]
        fade_in_window = np.linspace(0, 1, min(fade_in_samples, audio.shape[0] - first_zero_crossing), endpoint=False)

        for channel in range(audio.shape[1]):
            audio[:fade_in_samples, channel] *= fade_in_window
            max_value = np.max(np.abs(audio))
            audio = audio / max_value
            audio = audio * 10 ** (self.gain / 20)
            audio[:, channel] = np.clip(audio[:, channel], -self.threshold, self.threshold)
        return audio

    def find_loudness_settings(self, audio, sr, ref_loudness):
        search_space = np.linspace(0, 24, 1000)
        for gain in search_space:
            audio_copy = audio.copy()
            self.set_params([gain])
            audio_copy = self.process(audio_copy, sr)
            audio_loudness = loudness.get_loudness(audio_copy, sr)
            print("audio_loudness: ", audio_loudness, "ref_loudness: ", ref_loudness, "gain: ", gain)
            if audio_loudness >= ref_loudness:
                return gain

    def find_crest_settings(self, audio, sr, ref_crest):
        pass

    def find_set_settings(self, audio, sr, mode, ref_loudness=-7, ref_crest=2.8):
        if mode == "loudness":
            params = self.find_loudness_settings(audio, sr, ref_loudness)
            self.set_params([params])
            return params
        elif mode == "crest":
            params = self.find_crest_settings(audio, sr, ref_crest)
            self.set_params([params])
            return params
        else:
            raise ValueError("Invalid mode")
