import pedalboard
import numpy as np
import matplotlib.pyplot as plt
from backend import plugin
from backend import optimizer
from backend import constants
from backend import audio_utils
from backend import spectrum
from backend import loudness


class CustomEqualizer(plugin.Plugin):
    def __init__(self):
        super().__init__()
        self.board = pedalboard.Pedalboard([
                        pedalboard.HighpassFilter(cutoff_frequency_hz=30),
                        pedalboard.PeakFilter(cutoff_frequency_hz=100, gain_db=0, q=1),
                        pedalboard.PeakFilter(cutoff_frequency_hz=500, gain_db=0, q=1),
                        pedalboard.PeakFilter(cutoff_frequency_hz=1000, gain_db=0, q=1),
                        pedalboard.PeakFilter(cutoff_frequency_hz=2000, gain_db=0, q=1),
                        pedalboard.PeakFilter(cutoff_frequency_hz=4000, gain_db=0, q=1),
                        pedalboard.PeakFilter(cutoff_frequency_hz=6000, gain_db=0, q=1),
                        pedalboard.HighShelfFilter(cutoff_frequency_hz=7500, gain_db=0, q=1)])

    def set_params(self, values):
        self.board[1].gain_db = values[0]
        self.board[2].gain_db = values[1]
        self.board[3].gain_db = values[2]
        self.board[4].gain_db = values[3]
        self.board[5].gain_db = values[4]
        self.board[6].gain_db = values[5]
        self.board[7].gain_db = values[6]
        self.board[1].cutoff_frequency_hz = values[7]
        self.board[2].cutoff_frequency_hz = values[8]
        self.board[3].cutoff_frequency_hz = values[9]
        self.board[4].cutoff_frequency_hz = values[10]
        self.board[5].cutoff_frequency_hz = values[11]
        self.board[6].cutoff_frequency_hz = values[12]
        self.board[7].cutoff_frequency_hz = values[13]
        self.board[1].q = values[14]
        self.board[2].q = values[15]
        self.board[3].q = values[16]
        self.board[4].q = values[17]
        self.board[5].q = values[18]
        self.board[6].q = values[19]
        self.board[7].q = values[20]

    def process(self, audio, sr):
        return self.board(audio, sr)

        return processed_audio

    def find_set_settings(self, bounds, raw_mono, sr_raw, power_ref, maxiter=constants.NUM_ITERATIONS, verbose=True):
        """
        Finds the best settings for the Equalizer object
        :param bounds:
        :param raw_mono:
        :param sr_raw:
        :param power_ref:
        :param maxiter:
        :param verbose:
        :param mode:
        :return:
        """
        params = optimizer.dual_annealing_optimization(self, bounds, raw_mono, sr_raw, power_ref, maxiter=maxiter)
        params = [round(x, 1) for x in params.x]
        self.set_params(params)
        print("Best settings: ", params)
        return params


if __name__ == "__main__":

    audio, sr = audio_utils.load_audio_file("../tracks/raw_tracks/18.wav")
    audio_max_mono, audio_max_stereo = audio_utils.preprocess_audio(audio, sr, 10)

    audio_loudness = loudness.get_loudness(audio_max_mono, sr)

    ref, sr_ref = audio_utils.load_audio_file("../tracks/reference_tracks/02 - Sound of Madness.mp3")
    ref_max_mono, ref_max_stereo = audio_utils.preprocess_audio(ref, sr_ref, 10)

    ref_max_mono = loudness.equal_loudness(ref_max_mono, sr_ref, audio_loudness)


    eq = CustomEqualizer()

    gain = [1, 1, -11, 1, 1, 6, 6]
    freq = [100, 500, 750, 2000, 4000, 4000, 7500]
    q = [2, 1, 3, 3, 1, 0.5, 1]

    params = gain + freq + q

    eq.set_params(params)

    processed_max_mono = eq.process(audio_max_mono, sr)

    spec_raw, freq = spectrum.create_spectrum(audio_max_mono, sr)
    spec_processed, freq = spectrum.create_spectrum(processed_max_mono, sr)
    spec_ref, freq = spectrum.create_spectrum(ref_max_mono, sr_ref)

    #plt.plot(freq, spec_raw, label="raw")
    plt.plot(freq, spec_processed, label="processed")
    plt.plot(freq, spec_ref, label="ref")
    plt.legend()
    plt.xscale("log")
    plt.show()



