import numpy as np
import pedalboard
from reference_master.utils import loudness
from reference_master.plugins import plugin


class Clipper(plugin.Plugin):

    def __init__(self):
        """
        This class is a custom clipper that is used to clip the audio to a certain loudness
        """
        super().__init__()
        self.board = pedalboard.Pedalboard([pedalboard.Gain(gain_db=0), pedalboard.Clipping(-1.2)])

    def set_params(self, values):
        """
        Set the parameters of the clipper
        :param values: list of values to set the parameters to
        """
        self.board[0].gain_db = values[0]

    def find_loudness_settings(self, audio, sr, ref_loudness):
        """
        Find the settings for the clipper that will result in a certain loudness
        :param audio: audio to process
        :param sr: sample rate of the audio
        :param ref_loudness: loudness target
        :return: gain parameter which will result in the target loudness
        """
        search_space = np.linspace(0, 24, 1000)
        for gain in search_space:
            audio_copy = audio.copy()
            self.set_params([gain])
            audio_copy = self.process(audio_copy, sr)
            audio_loudness = loudness.get_loudness(audio_copy, sr)
            print("audio_loudness: ", audio_loudness, "ref_loudness: ", ref_loudness, "gain: ", gain)
            if audio_loudness >= ref_loudness:
                return gain

    def find_set_settings(self, audio, sr, ref_loudness):
        """
        Find the settings for the clipper that will result in a certain loudness or crest factor and
        set the parameters of the clipper to those values
        :param audio: audio to process
        :param sr: sample rate of the audio
        :param ref_loudness: target loudness
        :return: parameters that will result in the target loudness or crest factor
        """
        params = self.find_loudness_settings(audio, sr, ref_loudness)
        self.set_params([params])
        return params

