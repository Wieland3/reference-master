import pedalboard
import constants


def load_plugin(plugin_path):
    # this function should load a plugin from the plugin_path and return it
    return pedalboard.load_plugin(plugin_path)


def process(plugin, audio, sr):
    # this function should process the audio with the plugin and return the processed audio
    return plugin.process(audio, sr)


def set_plugin_params(plugin, values, mode):
    # this function should set all the specified parameters to the value
    plugin.__setattr__('1eq0_db', values[0]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq1_db', values[1]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq2_db', values[2]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq3_db', values[3]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq4_db', values[4]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq5_db', values[5]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq6_db', values[6]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq7_db', values[7]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq8_db', values[8]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq9_db', values[9]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq10_db', values[10]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq11_db', values[11]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq12_db', values[12]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq13_db', values[13]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq14_db', values[14]) # -12.0 to 12.0 in 0.1
    plugin.__setattr__('1eq15_db', values[15]) # -12.0 to 12.0 in 0.1

if __name__ == '__main__':
    eq = load_plugin(constants.PATH_TO_MARVEL_EQ_PLUGIN)
    eq.__setattr__('2eq0_db', -11)
    print(eq.parameters)
    eq.show_editor()
