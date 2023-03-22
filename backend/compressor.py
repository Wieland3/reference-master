import plugin
import constants
import audio_utils
import numpy as np

class Compressor(plugin.Plugin):
    def __init__(self, plugin_path):
        super().__init__(plugin_path)
        self.plugin.soft_knee_db = 4.0
        self.plugin.ratio = 2.0
        self.plugin.attack_ms = 20
        self.plugin.release_rm_ms = 400
        self.plugin.release_peak_ms = 60  # 25 - 100

    def set_params(self, values):
        self.plugin.threshold_db = values[0]  # -50 - 0

    def find_set_settings(self, audio, reference, audio_sr):
        rms_audio = audio_utils.rms(audio)
        rms_reference = audio_utils.rms(reference)
        seach_space = np.linspace(0, -50, 100)
        for threshold in seach_space:
            audio_copy = audio.copy()
            self.set_params([threshold])
            audio_copy = self.process(audio, audio_sr)
            rms_audio_copy = audio_utils.rms(audio_copy)
            print("rms_audio_copy: ", rms_audio_copy, "rms_reference: ", rms_reference, "threshold: ", threshold)
            if rms_audio_copy >= rms_reference:
                return threshold




comp = Compressor(constants.PATH_TO_KOTELNIKOV)
print(comp.plugin.parameters)
comp.show_editor()