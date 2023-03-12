import plugin
import constants

class SlickEq(plugin.Plugin):

    def __init__(self, plugin_path, shapes):
        super().__init__(plugin_path)
        self.plugin.low_shape = shapes[0]  # Shelf or Bell
        self.plugin.high_shape = shapes[1]  # Shelf or Bell
        self.plugin.auto_gain = False


    def set_params(self, values):
        self.plugin.low_gain_db = values[0]  # -18.0 to 18.0 in 0.1
        self.plugin.low_freq_hz = values[1]  # 30.0 to 1000.0 in 2.5
        self.plugin.mid_gain_db = values[2]  # -18.0 to 18.0 in 0.1
        self.plugin.mid_freq_hz = values[3]  # 100.0 to 10000.0 in 13.69
        self.plugin.high_gain_db = values[4]  # -18.0 to 18.0 in 0.1
        self.plugin.high_freq_hz = values[5]  # 500.0 to 40000.0 in 30.4
