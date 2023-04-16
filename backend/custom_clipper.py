import numpy as np
from backend import loudness


class CustomClipper:

    def __init__(self):
        """
        This class is a custom clipper that is used to clip the audio to a certain loudness
        """
        self.threshold = 10 ** (-1.2 / 20)
        self.gain = 0
        self.fade_in_duration = 0.1

    def set_params(self, values):
        """
        Set the parameters of the clipper
        :param values: list of values to set the parameters to
        """
        self.gain = values[0]

    def process(self, audio, sr):
        """
        Process the audio with the clipper
        :param audio: audio to process
        :param sr: sample rate of the audio
        :return: processed audio
        """
        # create a fade in window:
        fade_in_samples = int(self.fade_in_duration * sr)
        fade_in_window = np.exp(np.linspace(-5, 0, fade_in_samples))

        # append 0.1 seconds of silence in the beginning of the audio:
        audio = np.concatenate((np.zeros((fade_in_samples, audio.shape[1])), audio), axis=0)

        for channel in range(audio.shape[1]):
            max_value = np.max(np.abs(audio))
            audio = audio / max_value
            audio = audio * 10 ** (self.gain / 20)
            audio[fade_in_samples:2*fade_in_samples, channel] *= fade_in_window
            audio[:, channel] = np.clip(audio[:, channel], -self.threshold, self.threshold)
        return audio

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

    def find_crest_settings(self, audio, sr, ref_crest):
        pass

    def find_set_settings(self, audio, sr, mode, ref_loudness=-7, ref_crest=2.8):
        """
        Find the settings for the clipper that will result in a certain loudness or crest factor and
        set the parameters of the clipper to those values
        :param audio: audio to process
        :param sr: sample rate of the audio
        :param mode: mode to use to find the settings, can be "loudness" or "crest"
        :param ref_loudness: target loudness
        :param ref_crest: target crest factor
        :return: parameters that will result in the target loudness or crest factor
        """
        if mode == "loudness":
            params = self.find_loudness_settings(audio, sr, ref_loudness)
            self.set_params([params])
            return params
        elif mode == "crest":
            params = self.find_crest_settings(audio, sr, ref_crest)
            self.set_params([params])
            return params
        else:
            raise ValueError("Invalid mode")
