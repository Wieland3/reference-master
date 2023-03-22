import audio_utils
import optimizer
import constants
import time
import loudness
import audio_distance
import spectrum
import matplotlib.pyplot as plt
import nova_eq
import bsa_clipper

if __name__ == '__main__':

    # set constants
    duration = constants.DURATION

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file('../tracks/raw_tracks/9.wav')
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
    ref, sr_ref = audio_utils.load_audio_file('../tracks/reference_tracks/BreakTheFall.mp3')
    print("ref sr", sr_ref)

    ref_mono, ref_max = audio_utils.preprocess_audio(ref, sr_ref, duration)
    ref_loudness = loudness.get_loudness(ref_max, sr_ref)
    ref_loudness_adjusted = loudness.equal_loudness(ref_max, sr_ref, raw_loudness)
    print("loudness after adjust", loudness.get_loudness(ref_loudness_adjusted, sr_ref))
    ref_mono, _ = audio_utils.preprocess_audio(ref_loudness_adjusted, sr_ref, None)


    crest_raw = audio_utils.crest_factor(raw_mono)
    crest_ref = audio_utils.crest_factor(ref_mono)

    print("crest raw", crest_raw)
    print("crest ref", crest_ref)
    # Fit curves

    low_bounds = [(-17,17),(0.1,6),(30,250)]
    low_mid_bounds = [(-17,17),(0.1,6),(250, 2500)]
    high_mid_bounds = [(-17,17),(0.1,6),(2500, 7500)]
    high_bounds = [(-17,17),(0.1,6),(7500, 20000)]
    bounds = low_bounds + low_mid_bounds + high_mid_bounds + high_bounds

    eq = nova_eq.NovaEq(constants.PATH_TO_NOVA_PLUGIN)

    power_ref = spectrum.create_spectrum(ref_mono, sr_ref)
    init_dist = audio_distance.song_distance(raw_mono, sr_raw, power_ref)
    params = eq.find_set_settings(bounds, raw_mono, sr_raw, power_ref)
    eq.show_editor()
    processed = eq.process(raw_max, sr_raw)

    processed_copy = processed.copy()

    # Clipper
    clipper = bsa_clipper.BSAClipper(constants.PATH_TO_CLIPPER)
    setting = clipper.find_set_settings(processed_copy, sr_raw, mode='crest', ref_crest=crest_ref).round(1)
    print("clipper setting", setting)
    processed = clipper.process(processed, sr_raw)
    clipper.show_editor()
    final_loudness = loudness.get_loudness(processed, sr_raw)
    print("final loudness", final_loudness)
    print("final crest", audio_utils.crest_factor(processed))

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

    spec_raw, freq = spectrum.create_spectrum(raw, sr_raw)
    spec_ref, freq = spectrum.create_spectrum(ref, sr_ref)
    spec_pro, freq = spectrum.create_spectrum(processed, sr_raw)

    plt.plot(freq, spec_raw, label="raw")
    plt.plot(freq, spec_ref, label="ref")
    plt.plot(freq, spec_pro, label="processed")
    #plt.xscale('log')
    plt.grid(True, which="both", ls="-", color='0.65')
    plt.legend()
    plt.show()



