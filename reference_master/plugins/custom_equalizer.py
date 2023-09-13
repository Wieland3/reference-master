import pedalboard
from reference_master.plugins import plugin
from reference_master import optimizer
from reference_master import constants
from reference_master.utils import audio_utils, loudness, spectrum


class CustomEqualizer(plugin.Plugin):
    def __init__(self):
        super().__init__()
        self.filters = [pedalboard.HighpassFilter(cutoff_frequency_hz=30)]
        self.filters += [pedalboard.PeakFilter(cutoff_frequency_hz=cutoff, gain_db=0, q=1) for cutoff in
                       [100, 250, 500, 1000, 1000, 2000, 2000, 4000, 4000, 6000, 6000]]
        self.filters.append(pedalboard.HighShelfFilter(cutoff_frequency_hz=7500, gain_db=0, q=1))
        self.board = pedalboard.Pedalboard(self.filters)

    def set_filter_params(self, filter_index, gain_db, cutoff_frequency_hz, q):
        eq_filter = self.board[filter_index]
        eq_filter.gain_db = gain_db
        eq_filter.cutoff_frequency_hz = cutoff_frequency_hz
        eq_filter.q = q

    def set_params(self, values):
        num_filters = len(self.filters) - 1
        gain_idx_offset = num_filters
        q_idx_offset = num_filters * 2
        for i in range(num_filters):
            self.set_filter_params(i + 1, values[i], values[i + gain_idx_offset], values[i + q_idx_offset])

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

    audio, sr = audio_utils.load_audio_file("../../tracks/raw_tracks/18.wav")
    audio_max_mono, audio_max_stereo = audio_utils.preprocess_audio(audio, sr, 10)

    audio_loudness = loudness.get_loudness(audio_max_mono, sr)

    ref, sr_ref = audio_utils.load_audio_file("../../tracks/reference_tracks/02 - Sound of Madness.mp3")
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



