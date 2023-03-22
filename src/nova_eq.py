import plugin
import constants

class NovaEq(plugin.Plugin):

    def __init__(self, plugin_path):
        super().__init__(plugin_path)
        self.plugin.eq_auto_gain = False
        self.plugin.band_1_active = True
        self.plugin.band_2_active = True
        self.plugin.band_3_active = True
        self.plugin.band_4_active = True
        self.plugin.band_1_type = "Bell"
        self.plugin.band_2_type = "Bell"
        self.plugin.band_3_type = "Bell"
        self.plugin.band_4_type = "High S"

    def set_params(self, values):
        self.plugin.band_1_gain_db = values[0]  # -18.0 to 18.0
        self.plugin.band_1_q = values[1]  # 0.1 to 6.0
        self.plugin.band_1_frequency_hz = values[2]  # 10.0 to 40000.0
        self.plugin.band_2_gain_db = values[3]  # -18.0 to 18.0
        self.plugin.band_2_q = values[4]  # 0.1 to 6.0
        self.plugin.band_2_frequency_hz = values[5]  # 10.0 to 40000.0
        self.plugin.band_3_gain_db = values[6]  # -18.0 to 18.0
        self.plugin.band_3_q = values[7]  # 0.1 to 6.0
        self.plugin.band_3_frequency_hz = values[8]  # 10.0 to 40000.0
        self.plugin.band_4_gain_db = values[9]  # -18.0 to 18.0
        self.plugin.band_4_q = values[10]  # 0.1 to 6.0
        self.plugin.band_4_frequency_hz = values[11]  # 10.0 to 40000.0
        self.plugin.hp_active = True
        self.plugin.hp_frequency_hz = 30.0

'''
nova = NovaEq(constants.PATH_TO_NOVA_PLUGIN)
nova.set_params([5.0, 6, 100.0, 4, 0.5, 1000.0, 3, 1.0, 2500.0, 2, 1.0, 10000.0])
print(nova.plugin.parameters)
nova.show_editor()
'''
