import pedalboard
import numpy as np
from mastering.plugins import plugin
from mastering.utils import loudness


class CustomCompressor(plugin.Plugin):
    def __init__(self):
        super().__init__()
        self.board = pedalboard.Pedalboard([pedalboard.Compressor(threshold_db=0, ratio=2,
                                                                  attack_ms=10, release_ms=100),
                                            pedalboard.Gain(gain_db=0)])

    def set_params(self, values):
        self.board[0].threshold_db = values[0]
        self.board[1].gain_db = values[1]

    def find_set_settings(self, raw, sr_raw):
        raw_loudness = loudness.get_loudness(raw, sr_raw)
        search_space = np.linspace(0, -24, 100)
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

