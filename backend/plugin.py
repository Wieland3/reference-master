import pedalboard


class Plugin:
    def __init__(self, plugin_path):
        self.plugin = pedalboard.load_plugin(plugin_path)

    def set_params(self, values):
        pass

    def set_param(self, param, value):
        pass

    def process(self, audio, sr):
        pro = self.plugin.process(audio, sr, reset=False)
        return pro

    def show_editor(self):
        self.plugin.show_editor()
