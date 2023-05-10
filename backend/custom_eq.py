import numpy as np
from scipy.signal import lfilter
from backend import audio_utils
from backend import spectrum
import matplotlib.pyplot as plt


class CustomEq:
    def __init__(self):
        self.low_center_freq = 100
        self.low_Q = 1
        self.low_gain = 5
        self.low_mid_center_freq = 300
        self.low_mid_Q = 1
        self.low_mid_gain = -5
        self.mid_center_freq = 2500
        self.mid_Q = 1
        self.mid_gain = 5
        self.high_mid_center_freq = 5000
        self.high_mid_Q = 1
        self.high_mid_gain = 5
        self.high_center_freq = 7500
        self.high_Q = 0.1
        self.high_gain = 10

    def set_params(self, values):
        self.low_center_freq = values[0]
        self.low_Q = values[1]
        self.low_gain = values[2]
        self.low_mid_center_freq = values[3]
        self.low_mid_Q = values[4]
        self.low_mid_gain = values[5]
        self.mid_center_freq = values[6]
        self.mid_Q = values[7]
        self.mid_gain = values[8]
        self.high_mid_center_freq = values[9]
        self.high_mid_Q = values[10]
        self.high_mid_gain = values[11]
        self.high_center_freq = values[12]
        self.high_Q = values[13]
        self.high_gain = values[14]

    def process(self, audio, sr):
        filters = []
        filters.append(self.peaking_filter_coeffs(self.low_center_freq, self.low_Q, self.low_gain, sr))
        filters.append(self.peaking_filter_coeffs(self.low_mid_center_freq, self.low_mid_Q, self.low_mid_gain, sr))
        filters.append(self.peaking_filter_coeffs(self.mid_center_freq, self.mid_Q, self.mid_gain, sr))
        filters.append(self.peaking_filter_coeffs(self.high_mid_center_freq, self.high_mid_Q, self.high_mid_gain, sr))
        filters.append(self.peaking_filter_coeffs(self.high_center_freq, self.high_Q, self.high_gain, sr))

        for filter in filters:
            a, b = filter
            audio = lfilter(a,b, audio)

        return audio

    def find_set_settings(self):
        pass

    def peaking_filter_coeffs(self, center_freq, Q, gain, sr):
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


audio, sr = audio_utils.load_audio_file("../tracks/raw_tracks/0.wav")
audio_mono, audio_stereo = audio_utils.preprocess_audio(audio, sr, 10)
spec, freq = spectrum.create_spectrum(audio_mono, sr)
plt.plot(freq, spec)
plt.xscale('log')
plt.show()

eq = CustomEq()
audio_stereo = eq.process(audio_stereo, sr)
audio_mono, _ = audio_utils.preprocess_audio(audio_stereo, None)
spec, freq = spectrum.create_spectrum(audio_mono, sr)
plt.plot(freq, spec)
plt.xscale('log')
plt.show()
