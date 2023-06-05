import numpy as np
from scipy.signal import lfilter, filtfilt
import time
from backend import constants
from backend import optimizer
from backend import plugin


class CustomEq(plugin.Plugin):
    def __init__(self):
        """
        Initializes the CustomEq object
        """
        super().__init__()
        self.low_center_freq = 100
        self.low_Q = 1
        self.low_gain = 0
        #self.low_mid_center_freq = 300
        #self.low_mid_Q = 1
        #self.low_mid_gain = 0
        self.mid_center_freq = 2500
        self.mid_Q = 1
        self.mid_gain = 0
        #self.high_mid_center_freq = 5000
        #self.high_mid_Q = 1
        #self.high_mid_gain = 0
        self.high_center_freq = 7500
        self.high_Q = 1
        self.high_gain = 0

    def set_params(self, values):
        """
        Sets the parameters of the CustomEq object
        :param values:
        :return:
        """
        self.low_center_freq = values[0]
        self.low_Q = values[1]
        self.low_gain = values[2]
        #self.low_mid_center_freq = values[3]
        #self.low_mid_Q = values[4]
        #self.low_mid_gain = values[5]
        self.mid_center_freq = values[3]
        self.mid_Q = values[4]
        self.mid_gain = values[5]
        #self.high_mid_center_freq = values[9]
        #self.high_mid_Q = values[10]
        #self.high_mid_gain = values[11]
        self.high_center_freq = values[6]
        self.high_Q = values[7]
        self.high_gain = values[8]

    def process(self, audio, sr):
        """
        Process the audio with the CustomEq object
        :param audio:
        :param sr:
        :return:
        """
        filters = [self.peaking_filter_coeffs(self.low_center_freq, self.low_Q, self.low_gain, sr),
                   self.peaking_filter_coeffs(self.mid_center_freq, self.mid_Q, self.mid_gain, sr),
                   self.high_shelf_filter_coeffs(self.high_center_freq, self.high_gain, sr)]

        if audio.ndim == 1:
            for l_filter in filters:
                a, b = l_filter
                audio = filtfilt(a, b, audio)
            return audio

        for i, channel in enumerate(range(audio.shape[1])):
            for l_filter in filters:
                a, b = l_filter
                audio[:,i] = filtfilt(a,b, audio[:,i])
        return audio

    def find_set_settings(self, bounds, raw_mono, sr_raw, power_ref, maxiter=constants.NUM_ITERATIONS, verbose=True, mode="annealing"):
        """
        Finds the best settings for the CustomEq object
        :param bounds:
        :param raw_mono:
        :param sr_raw:
        :param power_ref:
        :param maxiter:
        :param verbose:
        :param mode:
        :return:
        """
        start_time = time.time()
        if mode == "direct":
            print("Direct optimization")
            params = optimizer.direct_optimization(self, bounds, raw_mono, sr_raw, power_ref, maxiter=maxiter)
            print("Params", params.x)
        elif mode == "annealing":
            print("Annealing optimization")
            params = optimizer.dual_annealing_optimization(self, bounds, raw_mono, sr_raw, power_ref, maxiter=maxiter)
        if verbose:
            print("Mininm distance", params.fun)
            print("--- %s seconds ---" % (time.time() - start_time))
        params = [round(x, 1) for x in params.x]
        self.set_params(params)
        return params

    def peaking_filter_coeffs(self, center_freq, Q, gain, sr):
        """
        Creates the peaking filter coefficients
        :param center_freq:
        :param Q:
        :param gain:
        :param sr:
        :return:
        """
        a = 10 ** (gain / 40)
        w0 = 2 * np.pi * center_freq / sr
        alpha = np.sin(w0) / (2 * Q)

        b0 = 1 + alpha * a
        b1 = -2 * np.cos(w0)
        b2 = 1 - alpha * a
        a0 = 1 + alpha / a
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha / a

        b = np.array([b0, b1, b2]) / a0
        a = np.array([a0, a1, a2]) / a0

        return b, a

    def high_shelf_filter_coeffs(self, freq, gain, sr):
        """
        Creates the high shelf filter coefficients
        :param freq:
        :param Q:
        :param gain:
        :param sr:
        :return: coefs of the filter
        """
        V = 10 ** (gain / 20)
        K = np.tan(np.pi * freq / sr)

        a0 = 1
        a1 = 2 * (K ** 2 - 1) / (1 + np.sqrt(2) * K + K ** 2)

        b0 = V / (1 + np.sqrt(2) * K + K ** 2)
        b1 = 2 * (K ** 2 - V) / (1 + np.sqrt(2) * K + K ** 2)

        b = [b0, b1]
        a = [a0, a1]

        return b, a
