from backend import audio_utils
from backend import spectrum
import matplotlib.pyplot as plt
from backend import custom_filter
from backend import optimizer
from backend import constants
import time


class CustomEq:
    def __init__(self, sr):
        self.band_0 = custom_filter.CustomFilter(20, 100, sr)
        self.band_1 = custom_filter.CustomFilter(100, 200, sr)
        self.band_2 = custom_filter.CustomFilter(200, 500, sr)
        self.band_3 = custom_filter.CustomFilter(500, 1000, sr)
        self.band_4 = custom_filter.CustomFilter(1000, 2500, sr)
        self.band_5 = custom_filter.CustomFilter(2500, 5000, sr)
        self.band_6 = custom_filter.CustomFilter(5000, 7500, sr)
        self.band_7 = custom_filter.CustomFilter(7500, 20000, sr)

    def set_params(self, values):
        self.band_0.set_gain(values[0])
        self.band_1.set_gain(values[1])
        self.band_2.set_gain(values[2])
        self.band_3.set_gain(values[3])
        self.band_4.set_gain(values[4])
        self.band_5.set_gain(values[5])
        self.band_6.set_gain(values[6])
        self.band_7.set_gain(values[7])

    def process(self, audio, sr):
        filtered_audio = [getattr(self, attr).filter_audio(audio) for attr in dir(self)
                          if isinstance(getattr(self, attr), custom_filter.CustomFilter)]
        return sum(filtered_audio)

    def find_set_settings(self, bounds, raw_mono, sr_raw, power_ref, maxiter=constants.NUM_ITERATIONS, verbose=True, mode="annealing"):
        start_time = time.time()
        if mode == "direct":
            print("Direct optimization")
            params = optimizer.direct_optimization(self, bounds, raw_mono, sr_raw, power_ref, maxiter=maxiter)
        elif mode == "annealing":
            print("Annealing optimization")
            params = optimizer.dual_annealing_optimization(self, bounds, raw_mono, sr_raw, power_ref, maxiter=maxiter)
        if verbose:
            print("Mininm distance", params.fun)
            print("--- %s seconds ---" % (time.time() - start_time))
        params = [round(x, 1) for x in params.x]
        self.set_params(params)
        return params





raw, sr = audio_utils.load_audio_file('../tracks/edited/raw.wav')
raw_mono, raw_stereo = audio_utils.preprocess_audio(raw, sr, duration=10)
spec_raw, freq = spectrum.create_spectrum(raw_mono, sr)
plt.plot(freq, spec_raw, label="raw")
plt.xscale('log')
plt.show()

eq = CustomEq(sr)
eq.set_params([1, 1, 1, 1, 1, 1, 1, 1])
filtered = eq.process(raw_mono, sr)
spec_filtered, freq = spectrum.create_spectrum(filtered, sr)
plt.plot(freq, spec_filtered, label="filtered")
plt.xscale('log')
plt.show()
