import pedalboard
from backend import plugin
from backend import optimizer
from backend import constants


class CustomEqualizer(plugin.Plugin):
    def __init__(self):
        super().__init__()
        self.board = pedalboard.Pedalboard([
            pedalboard.HighpassFilter(cutoff_frequency_hz=30),
            pedalboard.PeakFilter(cutoff_frequency_hz=100, q=1, gain_db=0),
            pedalboard.PeakFilter(cutoff_frequency_hz=500, q=1, gain_db=0),
            pedalboard.PeakFilter(cutoff_frequency_hz=2000, q=1, gain_db=0),
            pedalboard.PeakFilter(cutoff_frequency_hz=7500, q=1, gain_db=0),
            pedalboard.HighShelfFilter(cutoff_frequency_hz=12000, gain_db=0)])

    def set_params(self, values):
        self.board[1].gain_db = values[0]
        self.board[2].gain_db = values[1]
        self.board[3].gain_db = values[2]
        self.board[4].gain_db = values[3]
        self.board[5].gain_db = values[4]
        self.board[1].cutoff_frequency_hz = values[5]
        self.board[2].cutoff_frequency_hz = values[6]
        self.board[3].cutoff_frequency_hz = values[7]
        self.board[4].cutoff_frequency_hz = values[8]
        self.board[5].cutoff_frequency_hz = values[9]
        self.board[1].q = values[10]
        self.board[2].q = values[11]
        self.board[3].q = values[12]
        self.board[4].q = values[13]
        self.board[5].q = values[14]

    def process(self, audio, sr):
        return self.board(audio, sr)

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
        params = optimizer.direct_optimization(self, bounds, raw_mono, sr_raw, power_ref, maxiter=maxiter)
        params = [round(x, 1) for x in params.x]
        self.set_params(params)
        return params
