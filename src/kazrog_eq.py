import plugin
import constants


class KazrogEq(plugin.Plugin):

    def __init__(self, plugin_path):
        super().__init__(plugin_path)

    def set_params(self, values):
        self.plugin.eq50_eq_50 = values[0]
        self.plugin.eq130_eq_130 = values[1]
        self.plugin.eq320_eq_320 = values[2]
        self.plugin.eq800_eq_800 = values[3]
        self.plugin.eq2000_eq_2000 = values[4]
        self.plugin.eq5000_eq_5000 = values[5]
        self.plugin.eq12500_eq_12500 = values[6]

if __name__ == "__main__":
    eq = KazrogEq(constants.PATH_TO_KAZROQ_PLUGIN)
    print(eq.plugin.parameters)
