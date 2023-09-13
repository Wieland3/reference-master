"""
Contains code for parent class of all plugins.
"""

class Plugin:
    def __init__(self):
        """
        Initializes the Plugin
        """
        self.board = None

    def set_params(self, values):
        """
        Set the parameters of the plugin
        :param values: values to set the parameters to
        :return: None
        """
        pass

    def process(self, audio, sr):
        """
        Process the audio with the plugin
        :param audio: audio to process
        :param sr: sample rate of audio to process
        :return: processed audio
        """
        return self.board(audio, sr)
