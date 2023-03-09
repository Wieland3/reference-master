import audio_utils
import optimizer
import constants
import time
import spectogram
import numpy as np
import loudness
import audio_distance
import slick_eq

if __name__ == '__main__':

    # set constants
    min_setting = constants.MIN_SETTING_TDR
    max_setting = constants.MAX_SETTING_TDR
    path_to_eq_plugin = constants.PATH_TO_TDR_EQ_PLUGIN
    duration = constants.DURATION
    n_params = constants.N_PARAMS_TDR

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file('../tracks/raw_tracks/2.wav')
    print("raw sr",sr_raw)
    raw_loudness = loudness.get_loudness(raw, sr_raw)
    start = time.time()
    raw_mono, raw_max = audio_utils.preprocess_audio(raw, sr_raw, duration)
    print("preprocess time", time.time() - start)
    print("raw loudness", raw_loudness)

    # Load reference track
    ref, sr_ref = audio_utils.load_audio_file('../tracks/reference_tracks/BreakTheFall.mp3')
    print("ref sr",sr_ref)

    ref_loudness = loudness.get_loudness(ref, sr_ref)
    print("ref loudness before",ref_loudness)
    ref_loudness_adjusted = loudness.equal_loudness(ref, sr_ref, raw_loudness)
    ref_loudness = loudness.get_loudness(ref_loudness_adjusted, sr_ref)
    print("ref loudness after", ref_loudness)

    ref_mono, ref_max = audio_utils.preprocess_audio(ref_loudness_adjusted, sr_ref, duration)

    # Manual optimization
    #eq = eq_plugin.load_plugin(path_to_eq_plugin)
    #params = manual_optimizer.optimize(eq, raw_mono, ref_mono, sr_raw, sr_ref, 100)


    # Fit curves

    low_bounds = [(min_setting, max_setting), (30,1000)]
    mid_bounds = [(min_setting, max_setting), (100, 10000)]
    high_bounds = [(min_setting, max_setting), (500, 20000)]
    bounds = low_bounds + mid_bounds + high_bounds
    start_time = time.time()

    #eq = tdr_eq_plugin.load_plugin(path_to_eq_plugin)
    #tdr_eq_plugin.set_shape_params(eq, ["Bell", "Shelf"])

    eq = slick_eq.SlickEq(path_to_eq_plugin, ["Bell", "Shelf"])
    init_dist = audio_distance.song_distance(raw_mono, ref_mono, sr_raw, sr_ref, min_freq=0, max_freq=20000)
    params = optimizer.dual_annealing_optimization(eq, bounds, raw_mono, ref_mono, sr_raw, sr_ref,
                                                   min_freq=0, max_freq=20000, maxiter=100)
    print(params)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Initial Distance", init_dist)
    print("Minimum Distance", params.fun)
    params = [round(x, 1) for x in params.x]
    print("final low params", params)
    #params = [18.0, 0, 0, 100.0, 2500, 30000]
    # Process audio according to best params
    #eq = tdr_eq_plugin.load_plugin(path_to_eq_plugin)
    eq.set_params(params)
    processed = eq.process(raw_max, sr_raw)

    '''

    # Marvel
    bounds = [(min_setting, max_setting)] * 16
    eq = marvel.load_plugin(constants.PATH_TO_MARVEL_EQ_PLUGIN)
    start_time = time.time()
    params = optimizer.dual_annealing_optimization(eq, bounds, raw_mono, ref_mono, sr_raw, sr_ref,
                                                    mode = "all", min_freq=0, max_freq=20000, maxiter=100)
    print("--- %s seconds ---" % (time.time() - start_time))
    params = [round(x, 1) for x in params.x]
    print(params)
    marvel.set_plugin_params(eq, params, mode='all')
    processed = marvel.process(eq, raw_max, sr_raw)
    '''
    eq.show_editor()

    # Save audio
    audio_utils.numpy_to_wav(processed, sr_raw, '../tracks/edited/processed.wav')
    audio_utils.numpy_to_wav(ref_max, sr_ref, '../tracks/edited/reference.wav')
    audio_utils.numpy_to_wav(raw_max, sr_raw, '../tracks/edited/raw.wav')

    # Load back audio
    raw, sr = audio_utils.load_audio_file('../tracks/edited/raw.wav')
    raw, _ = audio_utils.preprocess_audio(raw, sr)
    ref, sr = audio_utils.load_audio_file('../tracks/edited/reference.wav')
    ref, _ = audio_utils.preprocess_audio(ref, sr)
    processed, sr = audio_utils.load_audio_file('../tracks/edited/processed.wav')
    processed, _ = audio_utils.preprocess_audio(processed, sr)

    # Create spectograms
    mel_spectogram_raw = spectogram.create_mel_spectogram(raw, sr, min_freq=0, max_freq=20000)
    mel_spectogram_ref = spectogram.create_mel_spectogram(ref, sr, min_freq=0, max_freq=20000)
    mel_spectogram_pro = spectogram.create_mel_spectogram(processed, sr, min_freq=0, max_freq=20000)

    # Create power spectograms
    average_raw = spectogram.create_power_spectogram(mel_spectogram_raw, constants.LOOKBACK)
    average_ref = spectogram.create_power_spectogram(mel_spectogram_ref, constants.LOOKBACK)
    average_pro = spectogram.create_power_spectogram(mel_spectogram_pro, constants.LOOKBACK)
    dif_after = average_pro - average_ref
    dif_before = average_raw - average_ref
    print("Euclidean Distance before", np.linalg.norm(dif_before))
    print("Euclidean Distance after", np.linalg.norm(dif_after))

    # Plot results
    spectogram.plot_power_spectogram(average_raw, average_ref, average_pro, dif_before, dif_after)


