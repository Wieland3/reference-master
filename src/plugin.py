import pedalboard


class Plugin:
    def __init__(self, plugin_path):
        self.plugin = pedalboard.load_plugin(plugin_path)

    def set_params(self, values):
        pass

    def process(self, audio, sr):
        return self.plugin.process(audio, sr)

    def show_editor(self):
        self.plugin.show_editor()
