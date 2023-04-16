from scipy.signal import butter, sosfilt
import numpy as np
import librosa
from backend import audio_utils
from backend import spectrum
import matplotlib.pyplot as plt
from backend import custom_filter


class CustomEq:
    def __init__(self, sr):
        self.sr = sr
        self.low_filter = custom_filter.CustomFilter(20, 100, self.sr)
        self.low_mid_filter = custom_filter.CustomFilter(100, 1000, self.sr)
        self.high_mid_filter = custom_filter.CustomFilter(1000, 7500, self.sr)
        self.high_filter = custom_filter.CustomFilter(7500, 20000, self.sr)

    def set_params(self, values):
        self.low_filter.set_params(values[:2])


    def process(self, audio):
        self.low_filter.filter_audio(audio)





raw, sr = audio_utils.load_audio_file('../tracks/edited/raw.wav')
raw_mono, raw_stereo = audio_utils.preprocess_audio(raw, sr, duration=10)
spec_raw, freq = spectrum.create_spectrum(raw_mono, sr)
plt.plot(freq, spec_raw, label="raw")
plt.xscale('log')
plt.show()

eq = CustomEq(sr)
eq.set_params([0, 0])
filtered = eq.process(raw_mono)
spec_filtered, freq = spectrum.create_spectrum(filtered, sr)
plt.plot(freq, spec_filtered, label="filtered")
plt.xscale('log')
plt.show()
