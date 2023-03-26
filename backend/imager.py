import plugin
import numpy as np
import loudness
import audio_utils
import constants


class Imager(plugin.Plugin):

    def __init__(self, plugin_path):
        super().__init__(plugin_path)

    def set_params(self, values):
        #self.plugin.gain_db = values[0]  # 0 - 24
        pass

    def find_set_settings(self, audio, sr, mode, ref_loudness=-7, ref_crest=2.8):
        pass

imager = Imager(constants.PATH_TO_IMAGER)
imager.show_editor()
