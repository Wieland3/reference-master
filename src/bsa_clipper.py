import plugin
import constants
import numpy as np
import loudness

class BSAClipper(plugin.Plugin):

    def __init__(self, plugin_path):
        super().__init__(plugin_path)
        self.plugin.threshold_db = -2

    def set_params(self, values):
        self.plugin.gain_db = values[0]  # 0 - 24

    def find_settings(self, audio, sr, ref_loudness):
        search_space = np.linspace(0, 24, 1000)
        for gain in search_space:
            audio_copy = audio.copy()
            self.set_params([gain])
            audio_copy = self.process(audio_copy, sr)
            audio_loudness = loudness.get_loudness(audio_copy, sr)
            print("audio_loudness: ", audio_loudness, "ref_loudness: ", ref_loudness, "gain: ", gain)
            if audio_loudness >= ref_loudness:
                return gain
