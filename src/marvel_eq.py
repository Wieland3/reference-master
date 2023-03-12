import plugin
import constants


class MarvelEq(plugin.Plugin):

    def __init__(self, plugin_path):
        super().__init__(plugin_path)

    def set_param(self, param, value):
        self.plugin.__setattr__(param, value)

    def set_params(self, values):
        #self.plugin.__setattr__('1eq0_db', values[0])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq1_db', values[1])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq2_db', values[2])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq3_db', values[3])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq4_db', values[4])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq5_db', values[5])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq6_db', values[6])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq7_db', values[7])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq8_db', values[8])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq9_db', values[9])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq10_db', values[10])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq11_db', values[11])  # -12.0 to 12.0 in 0.1
        #self.plugin.__setattr__('1eq12_db', values[12])  # -12.0 to 12.0 in 0.1
        self.plugin.__setattr__('1eq13_db', values[0])  # -12.0 to 12.0 in 0.1
        self.plugin.__setattr__('1eq14_db', values[1])  # -12.0 to 12.0 in 0.1
        self.plugin.__setattr__('1eq15_db', values[2])  # -12.0 to 12.0 in 0.1

if __name__ == "__main__":
    eq = KazrogEq(constants.PATH_TO_KAZROQ_PLUGIN)
    print(eq.plugin.parameters)
