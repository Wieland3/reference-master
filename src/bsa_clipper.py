import plugin
import constants
import numpy as np
import loudness
import audio_utils


class BSAClipper(plugin.Plugin):

    def __init__(self, plugin_path):
        super().__init__(plugin_path)
        self.plugin.threshold_db = -2

    def set_params(self, values):
        self.plugin.gain_db = values[0]  # 0 - 24

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
        search_space = np.linspace(0, 24, 1000)
        for gain in search_space:
            audio_copy = audio.copy()
            self.set_params([gain])
            audio_copy = self.process(audio_copy, sr)
            audio_crest = audio_utils.crest_factor(audio_copy)
            print("audio_crest: ", audio_crest, "ref_crest: ", ref_crest, "gain: ", gain)
            if audio_crest <= ref_crest:
                return gain

    def find_settings(self, audio, sr, mode, ref_loudness=-7, ref_crest=2.8):
        if mode == "loudness":
            return self.find_loudness_settings(audio, sr, ref_loudness)
        elif mode == "crest":
            return self.find_crest_settings(audio, sr, ref_crest)
        else:
            raise ValueError("Invalid mode")

