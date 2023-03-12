import audio_utils
import optimizer
import constants
import time
import numpy as np
import loudness
import audio_distance
import slick_eq
from sklearn.preprocessing import MinMaxScaler
import spectrum
import matplotlib.pyplot as plt
import kazrog_eq
import marvel_eq
import nova_eq

if __name__ == '__main__':

    # set constants
    min_setting = constants.MIN_SETTING_TDR
    max_setting = constants.MAX_SETTING_TDR
    path_to_eq_plugin = constants.PATH_TO_TDR_EQ_PLUGIN
    duration = constants.DURATION
    n_params = constants.N_PARAMS_TDR

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file('../tracks/raw_tracks/13.wav')
    print("raw sr", sr_raw)
    raw_mono, raw_max = audio_utils.preprocess_audio(raw, sr_raw, duration)
    raw_loudness = loudness.get_loudness(raw_max, sr_raw)
    print("raw loudness", raw_loudness)

    # Load reference track
    ref, sr_ref = audio_utils.load_audio_file('../tracks/reference_tracks/BreakTheFall.mp3')
    print("ref sr", sr_ref)

    ref_mono, ref_max = audio_utils.preprocess_audio(ref, sr_ref, duration)
    ref_loudness = loudness.get_loudness(ref_max, sr_ref)
    ref_loudness_adjusted = loudness.equal_loudness(ref_max, sr_ref, raw_loudness)
    print("loudness after adjust", loudness.get_loudness(ref_loudness_adjusted, sr_ref))
    ref_mono, _ = audio_utils.preprocess_audio(ref_loudness_adjusted, sr_ref, None)


    # Fit curves
    #low_bounds = [(min_setting, max_setting), (30,250)]
    #mid_bounds = [(min_setting, max_setting), (5000, 7500)]
    #high_bounds = [(min_setting, max_setting), (2500, 20000)]
    #bounds = low_bounds + mid_bounds + high_bounds

    low_bounds = [(-17,17),(0.1,6),(30,250)]
    low_mid_bounds = [(-17,17),(0.1,6),(250, 2500)]
    high_mid_bounds = [(-17,17),(0.1,6),(2500, 10000)]
    high_bounds = [(-17,17),(0.1,6),(10000, 20000)]
    bounds = low_bounds + low_mid_bounds + high_mid_bounds + high_bounds
    start_time = time.time()

    #eq = slick_eq.SlickEq(path_to_eq_plugin, ["Bell", "Shelf"])
    eq = nova_eq.NovaEq(constants.PATH_TO_NOVA_PLUGIN)

    init_dist = audio_distance.song_distance(raw_mono, ref_mono, sr_raw, sr_ref)
    params = optimizer.dual_annealing_optimization(eq, bounds, raw_mono, ref_mono, sr_raw, sr_ref, maxiter=50)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Initial Distance", init_dist)
    print("Minimum Distance", params.fun)
    params = [round(x, 1) for x in params.x]
    print("final low params", params)
    eq.set_params(params)
    eq.show_editor()
    processed = eq.process(raw_max, sr_raw)

    # Show EQ

    # Save audio
    audio_utils.numpy_to_wav(processed, sr_raw, '../tracks/edited/processed.wav')
    audio_utils.numpy_to_wav(ref_loudness_adjusted, sr_ref, '../tracks/edited/reference.wav')
    audio_utils.numpy_to_wav(raw_max, sr_raw, '../tracks/edited/raw.wav')

    # Load back audio
    raw, sr = audio_utils.load_audio_file('../tracks/edited/raw.wav')
    raw, _ = audio_utils.preprocess_audio(raw, sr)
    ref, sr = audio_utils.load_audio_file('../tracks/edited/reference.wav')
    ref, _ = audio_utils.preprocess_audio(ref, sr)
    processed, sr = audio_utils.load_audio_file('../tracks/edited/processed.wav')
    processed, _ = audio_utils.preprocess_audio(processed, sr)

    spec_raw, freq = spectrum.create_spectrum(raw, sr_raw)
    spec_ref, freq = spectrum.create_spectrum(ref, sr_ref)
    spec_pro, freq = spectrum.create_spectrum(processed, sr_raw)

    plt.plot(freq,spec_raw, label="raw")
    plt.plot(freq,spec_ref, label="ref")
    plt.plot(freq,spec_pro, label="processed")
    plt.legend()
    plt.show()
