import audio_utils
import constants
import loudness
import audio_distance
import spectrum
import matplotlib.pyplot as plt
import nova_eq
import bsa_clipper
import mjuc
import custom_clipper

if __name__ == '__main__':

    # set constants
    duration = constants.DURATION

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file('../tracks/raw_tracks/22.mp3')
    print("raw sr", sr_raw)
    raw_mono, raw_max = audio_utils.preprocess_audio(raw, sr_raw, duration)

    '''
    if sr_raw != 44100:
        raw_mono = librosa.resample(raw_mono, orig_sr=sr_raw, target_sr=44100)
        raw_max = librosa.resample(raw_max, orig_sr=sr_raw, target_sr=44100)
    '''
    raw_loudness = loudness.get_loudness(raw_max, sr_raw)
    print("raw loudness", raw_loudness)

    # Load reference track
    ref, sr_ref = audio_utils.load_audio_file('../tracks/reference_tracks/01 - Nightmare [Explicit].mp3')
    print("ref sr", sr_ref)

    ref_mono, ref_max = audio_utils.preprocess_audio(ref, sr_ref, duration)
    ref_loudness = loudness.get_loudness(ref_max, sr_ref)
    print("ref loudness", ref_loudness)
    ref_loudness_adjusted = loudness.equal_loudness(ref_max, sr_ref, raw_loudness)
    print("loudness after adjust", loudness.get_loudness(ref_loudness_adjusted, sr_ref))
    crest_ref = audio_utils.crest_factor(ref_mono)
    ref_mono, _ = audio_utils.preprocess_audio(ref_loudness_adjusted, sr_ref, None)


    crest_raw = audio_utils.crest_factor(raw_mono)

    print("crest raw", crest_raw)
    print("crest ref", crest_ref)

    power_ref = spectrum.create_spectrum(ref_mono, sr_ref)
    init_dist = audio_distance.song_distance(raw_mono, sr_raw, power_ref)

    # Slick Eq
    #bounds = [(-18,18),(30,500),(-18,18),(500,7500),(-18,18),(7500,20000)]
    #slick = slick_eq.SlickEq(constants.PATH_TO_SLICK_EQ)
    #slick.find_set_settings(bounds, raw_mono, sr_raw, power_ref)
    #slick.show_editor()
    #raw_max = slick.process(raw_max, sr_raw)
    #raw_mono = audio_utils.preprocess_audio(raw_max, sr_raw, None)[0]

    # MJUC
    mjuc = mjuc.MJUC(constants.PATH_TO_MJUC)
    mjuc.find_set_settings(raw_max, sr_raw)
    processed = mjuc.process(raw_max, sr_raw)
    raw_mono = audio_utils.preprocess_audio(processed, sr_raw, None)[0]
    loudness_after = loudness.get_loudness(processed, sr_raw)
    print("loudness after", loudness_after)
    mjuc.show_editor()
    raw = mjuc.process(raw, sr_raw)

    # Nova Eq
    low_bounds = [(-17,17),(0.1,6),(30,100)]
    low_mid_bounds = [(-17,17),(0.1,6),(100, 1000)]
    high_mid_bounds = [(-17,17),(0.1,6),(1000, 7500)]
    high_bounds = [(-17,17),(0.1,6),(7500, 20000)]
    bounds = low_bounds + low_mid_bounds + high_mid_bounds + high_bounds

    eq = nova_eq.NovaEq(constants.PATH_TO_NOVA_PLUGIN, "High S")

    params = eq.find_set_settings(bounds, raw_mono, sr_raw, power_ref, mode='direct')
    processed = eq.process(processed, sr_raw)
    processed_mono = audio_utils.preprocess_audio(processed, sr_raw, None)[0]
    distance_after = audio_distance.song_distance(processed_mono, sr_raw, power_ref)

    print("distance before", init_dist)
    print("distance after", distance_after)
    eq.show_editor()
    raw = eq.process(raw, sr_raw)

    '''
    eq2 = nova_eq.NovaEq(constants.PATH_TO_NOVA_PLUGIN, "Bell")
    params2 = eq2.find_set_settings(bounds, processed_mono, sr_raw, power_ref)
    processed = eq2.process(processed, sr_raw)
    eq2.show_editor()
    raw = eq2.process(raw, sr_raw)
    '''

    # Clipper
    clipper = custom_clipper.CustomClipper()
    setting = clipper.find_set_settings(processed, sr_raw, mode='loudness', ref_loudness=ref_loudness).round(1)
    print("clipper setting", setting)
    processed = clipper.process(processed)
    #clipper.show_editor()
    final_loudness = loudness.get_loudness(processed, sr_raw)
    print("final loudness", final_loudness)
    print("final crest", audio_utils.crest_factor(processed))

    # clipper on raw max
    #raw_max = clipper.process(raw_max)
    raw = clipper.process(raw)
    # Save audio
    audio_utils.numpy_to_wav(processed, sr_raw, '../tracks/edited/processed.wav')
    audio_utils.numpy_to_wav(ref_max, sr_ref, '../tracks/edited/reference.wav')
    audio_utils.numpy_to_wav(raw_max, sr_raw, '../tracks/edited/raw.wav')
    audio_utils.numpy_to_wav(raw, sr_raw, '../tracks/edited/full.wav')

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

    plt.plot(freq, spec_raw, label="raw")
    plt.plot(freq, spec_ref, label="ref")
    plt.plot(freq, spec_pro, label="processed")
    plt.xscale('log')
    plt.grid(True, which="both", ls="-", color='0.65')
    plt.legend()
    plt.show()



