import numpy as np
from scipy.signal import lfilter


class Biquad:
    def __init__(self, sample_rate, filter_type=None, fc=1000, bandwidth=1.0, gain_db=1.0):
        """
        Initialize a biquad filter
        :param sample_rate: sample rate of the audio
        :param filter_type: type of the filter can be 'LowPass', 'HighPass', 'BandPass', 'Notch', 'Peak', 'LowShelf', 'HighShelf'
        :param fc: fc of the filter
        :param bandwidth: bandwidth of the filter
        :param gain_db: gain in db of the filter
        """
        self.sample_rate = sample_rate
        self.b = np.zeros(3)
        self.a = np.zeros(3)
        self.a[0] = 1.0
        self.b[0] = 1.0
        self.y = None
        self.x_buf = np.zeros(2)
        self.y_buf = np.zeros(2)
        self.filter_type = filter_type

        if fc < 0.0 or fc >= self.sample_rate / 2.0:
            raise ValueError(f"illegal value: fc={fc}")
        self._fc = fc

        self._gain_db = gain_db
        A = 10.0 ** (gain_db / 40.0)
        A_add_1 = A + 1.0
        A_sub_1 = A - 1.0
        sqrt_A = np.sqrt(A)

        w0 = 2.0 * np.pi * self._fc / self.sample_rate
        cos_w0 = np.cos(w0)
        sin_w0 = np.sin(w0)
        alpha = 0.5 * sin_w0 * fc / bandwidth

        if filter_type == "LowPass":
            self.set_low_pass_coefs(cos_w0, alpha)

        elif filter_type == "HighPass":
            self.set_high_pass_coefs(cos_w0, alpha)

        elif filter_type == "Peaking":
            self.set_peaking_coefs(cos_w0, alpha, A)

        elif filter_type == "LowShelf":
            self.set_low_shelf_coefs(A, A_add_1, A_sub_1, cos_w0, alpha, sqrt_A)

        elif filter_type == "HighShelf":
            self.set_high_shelf_coefs(A, A_add_1, A_sub_1, cos_w0, alpha, sqrt_A)

        self.b /= self.a[0]
        self.a /= self.a[0]

    def set_low_pass_coefs(self, cos_w0, alpha):
        self.b[0] = (1.0 - cos_w0) * 0.5
        self.b[1] = (1.0 - cos_w0)
        self.b[2] = (1.0 - cos_w0) * 0.5
        self.a[0] = 1.0 + alpha
        self.a[1] = -2.0 * cos_w0
        self.a[2] = 1.0 - alpha

    def set_high_pass_coefs(self, cos_w0, alpha):
        self.b[0] = (1.0 + cos_w0) * 0.5
        self.b[1] = -(1.0 + cos_w0)
        self.b[2] = (1.0 + cos_w0) * 0.5
        self.a[0] = 1.0 + alpha
        self.a[1] = -2.0 * cos_w0
        self.a[2] = 1.0 - alpha

    def set_peaking_coefs(self, cos_w0, alpha, A):
        if A != 1.0:
            self.b[0] = 1.0 + alpha * A
            self.b[1] = -2.0 * cos_w0
            self.b[2] = 1.0 - alpha * A
            self.a[0] = 1.0 + alpha / A
            self.a[1] = -2.0 * cos_w0
            self.a[2] = 1.0 - alpha / A

    def set_low_shelf_coefs(self, A, A_add_1, A_sub_1, cos_w0, alpha, sqrt_A):
        if A != 1.0:
            self.b[0] = A * (A_add_1 - A_sub_1 * cos_w0 + 2 * sqrt_A * alpha)
            self.b[1] = 2 * A * (A_sub_1 - A_add_1 * cos_w0)
            self.b[2] = A * (A_add_1 - A_sub_1 * cos_w0 - 2 * sqrt_A * alpha)
            self.a[0] = A_add_1 + A_sub_1 * cos_w0 + 2 * sqrt_A * alpha
            self.a[1] = -2 * (A_sub_1 + A_add_1 * cos_w0)
            self.a[2] = A_add_1 + A_sub_1 * cos_w0 - 2 * sqrt_A * alpha

    def set_high_shelf_coefs(self, A, A_add_1, A_sub_1, cos_w0, alpha, sqrt_A):
        if A != 1.0:
            self.b[0] = A * (A_add_1 + A_sub_1 * cos_w0 + 2 * sqrt_A * alpha)
            self.b[1] = -2 * A * (A_sub_1 + A_add_1 * cos_w0)
            self.b[2] = A * (A_add_1 + A_sub_1 * cos_w0 - 2 * sqrt_A * alpha)
            self.a[0] = A_add_1 - A_sub_1 * cos_w0 + 2 * sqrt_A * alpha
            self.a[1] = 2 * (A_sub_1 - A_add_1 * cos_w0)
            self.a[2] = A_add_1 - A_sub_1 * cos_w0 - 2 * sqrt_A * alpha

    def process_array_with_lfilter(self, audio):
        """
        Process an array of samples with lfilter
        :param audio: audio to filter
        :return: filtered audio
        """
        audio_copy = np.copy(audio)
        filtered = lfilter(self.b, self.a, audio_copy)
        return filtered
