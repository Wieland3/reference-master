from backend import biquad
from backend import audio_utils
from backend import spectrum
from backend import plugin
from backend import optimizer
from backend import constants
import matplotlib.pyplot as plt
import numpy as np
import time

center_freqs = [25, 31, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600,
                2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000]

band_widths = [10 for _ in range(len(center_freqs))]


class Equalizer(plugin.Plugin):
    def __init__(self, sr):
        """
        Initializes the Equalizer object
        :param sr: Sample rate of audio to be processed with the Equalizer object
        """
        super().__init__()
        self.sr = sr  # sample rate
        self.center_freqs = center_freqs  # center frequencies of the bands
        self.band_widths = band_widths  # bandwidths of the bands
        self.gains = [0 for _ in range(len(center_freqs))]  # gains of the bands
        self.num_bands = len(center_freqs)  # number of bands
        self.filters = []  # list of biquad filters

        for i in range(self.num_bands):
            self.filters.append(biquad.Biquad(self.sr, 'Peaking', self.center_freqs[i], self.band_widths[i], 0))

    def set_params(self, values):
        """
        Sets the parameters of the Equalizer object
        :param values: list of gains. Needs to have length equal to the number of bands
        :return: None
        """
        #self.center_freqs = values[0:self.num_bands]
        self.band_widths = values[0:self.num_bands]
        self.gains = values[self.num_bands:2 * self.num_bands]

        self.filters = []  # empty list of filters

        for i in range(self.num_bands):
            self.filters.append(biquad.Biquad(self.sr, 'Peaking', self.center_freqs[i], self.band_widths[i], self.gains[i]))

    def process(self, audio):
        """
        Process the audio with the equalizer. Can be mono or stereo
        :param audio: ndarray of audio
        :return:
        """
        audio_copy = audio.copy()  # copy audio to avoid modifying the original
        if audio.ndim == 1:  # if data is mono shape
            audio_copy = audio_copy.reshape(-1, 1)  # convert it to (samples, channel) format
        out = np.zeros(audio_copy.shape)  # create empty array for output

        for channel in range(audio_copy.shape[1]):  # for each channel
            out[:, channel] = self.process_channel_buffer(audio_copy[:, channel])  # process

        if audio_copy.shape[1] == 1:  # if data is mono
            out = out.reshape(-1,)  # convert it to back (samples,) format
        return out

    def process_channel_buffer(self, x):
        """
        Process a buffer of audio samples with the equalizer
        :param x: audio buffer to process
        :return: processed buffer
        """
        out = x.copy()
        for eq_filter in self.filters:
            out = eq_filter.process_array_with_lfilter(out)
        return out

    def find_set_settings(self, bounds, raw_mono, sr_raw, power_ref, maxiter=constants.NUM_ITERATIONS, verbose=True, mode="direct"):
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

'''
# load audio file
raw, sr = audio_utils.load_audio_file('../tracks/raw_tracks/0.wav')
raw_mono, raw_stereo = audio_utils.preprocess_audio(raw, sr, 10)

spec, freq = spectrum.create_spectrum(raw_mono, sr)

# create equalizer
eq = Equalizer(sr)
eq.set_params([-2, 0, 2, 2, 2, -2, 2, -2, -5, 10])
y = eq.process(raw_stereo)


# save edited audio
audio_utils.numpy_to_wav(y, sr, '../tracks/edited/0.wav')

y = audio_utils.preprocess_audio(y, sr, 10)[0]
spec_eq, freq_eq = spectrum.create_spectrum(y, sr)

plt.plot(freq, spec, label="unedited")
plt.plot(freq_eq, spec_eq, label="edited")
plt.legend()
plt.xscale('log')
plt.show()
'''



