import sys
sys.path.append('../')
from backend import plugin
from backend import constants
from backend import loudness
import numpy as np


class MJUC(plugin.Plugin):
    def __init__(self, plugin_path):
        super().__init__(plugin_path)
        self.plugin.timing = "fast"

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
            if raw_loudness - raw_copy_loudness > constants.REDUCE:
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
