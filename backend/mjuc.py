import plugin
import constants
import audio_utils
import numpy as np
import loudness
import optimizer
import bsa_clipper

class MJUC(plugin.Plugin):
    def __init__(self, plugin_path):
        super().__init__(plugin_path)
        self.plugin.timing = "auto"

    def set_params(self, values):
        self.plugin.compress = values[0]  # 0 - 48
        self.plugin.makeup = values[1]  # -12 - 36

    def find_set_settings(self, raw, sr_raw):
        raw_loudness = loudness.get_loudness(raw, sr_raw)
        search_space = np.linspace(0, 48, 100)
        compress_setting = 0
        for compress in search_space:
            raw_copy = raw.copy()
            self.set_params([compress, 0])
            raw_copy = self.process(raw_copy, sr_raw)
            raw_copy_loudness = loudness.get_loudness(raw_copy, sr_raw)
            if raw_loudness - raw_copy_loudness > 2:
                compress_setting = compress
                break
        search_space = np.linspace(0, 36, 100)
        for makeup in search_space:
            raw_copy = raw.copy()
            self.set_params([compress_setting, makeup])
            raw_copy = self.process(raw_copy, sr_raw)
            raw_copy_loudness = loudness.get_loudness(raw_copy, sr_raw)
            if raw_loudness - raw_copy_loudness < 0:
                self.set_params([compress_setting, makeup])
                return [compress_setting, makeup]



'''
# Load raw track
raw, sr_raw = audio_utils.load_audio_file('../tracks/raw_tracks/18.wav')
raw_mono, raw_max = audio_utils.preprocess_audio(raw, sr_raw, constants.DURATION)

loudness_before = loudness.get_loudness(raw_max, sr_raw)
crest_before = audio_utils.crest_factor(raw_max)
rms_before = audio_utils.rms(raw_max)
print("loudness_before: ", loudness_before, "crest_before: ", crest_before, "rms_before: ", rms_before)

comp = MJUC(constants.PATH_TO_MJUC)
params = comp.find_set_settings(raw_max, sr_raw)
print("params: ", params)
processed = comp.process(raw_max, sr_raw)
loudness_after = loudness.get_loudness(processed, sr_raw)
crest_after = audio_utils.crest_factor(processed)
rms_after = audio_utils.rms(processed)
print("loudness_after: ", loudness_after, "crest_after: ", crest_after, "rms_after: ", rms_after)
comp.show_editor()
'''