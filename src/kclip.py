import plugin
import constants


class KClip(plugin.Plugin):
        def __init__(self, plugin_path):
            super().__init__(plugin_path)

        def set_params(self, values):
            pass

if __name__ == "__main__":
    clip = KClip(constants.PATH_TO_KCLIP_PLUGIN)

