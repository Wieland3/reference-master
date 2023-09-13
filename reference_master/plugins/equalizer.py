"""
File contains code for the Equalizer Plugin.
"""


import pedalboard
from reference_master.plugins import plugin
from reference_master.mastering import optimizer
from reference_master import constants


class Equalizer(plugin.Plugin):
    def __init__(self):
        """
        Initializes the Equalizer Plugin
        """
        super().__init__()
        self.filters = [pedalboard.HighpassFilter(cutoff_frequency_hz=30)]
        self.filters += [pedalboard.PeakFilter(cutoff_frequency_hz=cutoff, gain_db=0, q=1) for cutoff in
                       [100, 250, 500, 1000, 1000, 2000, 2000, 4000, 4000, 6000, 6000]]
        self.filters.append(pedalboard.HighShelfFilter(cutoff_frequency_hz=7500, gain_db=0, q=1))
        self.board = pedalboard.Pedalboard(self.filters)

    def set_filter_params(self, filter_index, gain_db, cutoff_frequency_hz, q):
        """
        Set the parameters of an individual filter
        :param filter_index: index of filter in the board
        :param gain_db: gain in dB
        :param cutoff_frequency_hz: cutoff frequency in Hz
        :param q: q value of the filter
        :return: None
        """
        eq_filter = self.board[filter_index]
        eq_filter.gain_db = gain_db
        eq_filter.cutoff_frequency_hz = cutoff_frequency_hz
        eq_filter.q = q

    def set_params(self, values):
        """
        Set the parameters of the equalizer
        :param values: list of parameters for filters in form [gain1, gain2, ..., gain12, cutoff1, cutoff2, ..., cutoff12, q1, q2, ..., q12]
        :return: None
        """
        num_filters = len(self.filters) - 1
        gain_idx_offset = num_filters
        q_idx_offset = num_filters * 2
        for i in range(num_filters):
            self.set_filter_params(i + 1, values[i], values[i + gain_idx_offset], values[i + q_idx_offset])

    def find_set_settings(self, bounds, raw_mono, sr_raw, power_ref, maxiter=constants.NUM_ITERATIONS):
        """
        Finds the best settings for the Equalizer object
        :param bounds: bounds for the parameters
        :param raw_mono: mono version of the raw track
        :param sr_raw: sample rate of the raw track
        :param power_ref: reference power spectrum
        :param maxiter: maximum number of iterations
        :return: best settings for the equalizer
        """
        params = optimizer.dual_annealing_optimization(self, bounds, raw_mono, sr_raw, power_ref, maxiter=maxiter)
        params = [round(x, 1) for x in params.x]
        self.set_params(params)
        print("Best settings: ", params)
        return params
