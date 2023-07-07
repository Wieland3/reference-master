from mastering import audio_utils
from mastering import constants
from mastering import loudness
from mastering import spectrum
from mastering.plugins import custom_equalizer, custom_clipper
import os
import numpy as np
import matplotlib.pyplot as plt


def master(audiofile):
    duration = constants.DURATION
    path = "../tracks/raw_tracks/" + audiofile

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file("../uploads/" + path)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)

    # Bring the raw track to the same loudness as the reference tracks to find the closest reference track
    raw_max_loudness_adjusted_stereo = loudness.equal_loudness(raw_max_stereo, sr_raw, constants.LOUDNESS_NORM)
    raw_max_loudness_adjusted_mono, _ = audio_utils.preprocess_audio(raw_max_loudness_adjusted_stereo, sr_raw, None)

    # Find the closest reference track
    #db = song_database.SpectrumDatabase()
    #db.load_spectrum_database()
    #closest_track = db.find_closest(raw_max_loudness_adjusted_mono, sr_raw)

    # Load closest reference track
    ref, sr_ref = audio_utils.load_audio_file("../tracks/reference_tracks/BreakTheFall.mp3")
    ref_max_mono, ref_max_stereo = audio_utils.preprocess_audio(ref, sr_ref, duration)

    # Loudness Calculation
    raw_loudness = loudness.get_loudness(raw_max_stereo, sr_raw)
    ref_loudness = loudness.get_loudness(ref_max_stereo, sr_ref)
    print(ref_loudness)

    # Make sure the reference track is the same loudness as the raw track
    ref_max_loudness_adjusted_stereo = loudness.equal_loudness(ref_max_stereo, sr_ref, raw_loudness)
    ref_max_mono, _ = audio_utils.preprocess_audio(ref_max_loudness_adjusted_stereo, sr_ref, None)

    # Reference Spectrum Calculation
    power_ref, freq = spectrum.create_spectrum(ref_max_mono, sr_ref)

    center_freqs = [(30, 100), (100, 250), (250, 500), (1000, 2000), (1500, 2500), (2000, 3000), (2500, 3500), (3000, 4000), (3500, 4500), (4000, 5000), (4500, 7500), (7500, 16000)]
    Q_values = [(0.1, 6) for _ in range(12)]
    gain = [(-16.0, 16.0) for _ in range(12)]
    bounds = gain + center_freqs + Q_values

    print("Bounds", bounds)
    print("LEN", len(bounds))
    eq = custom_equalizer.CustomEqualizer()

    eq.find_set_settings(bounds, raw_max_mono, sr_raw, power_ref)
    raw_max_stereo = eq.process(raw_max_stereo, sr_raw)  # Apply Eq to entire track
    raw_max_mono, _ = audio_utils.preprocess_audio(raw_max_stereo, sr_raw, None)
    raw = eq.process(raw, sr_raw)  # Apply Eq to entire track

    print("max before clip", np.max(raw))
    print("min before clip", np.min(raw))
    # Clipper
    clipper = custom_clipper.CustomClipper()
    print("reference loudness", ref_loudness)
    clipper.find_set_settings(raw_max_stereo, sr_raw, ref_loudness=ref_loudness)

    raw_max_stereo = clipper.process(raw_max_stereo, sr_raw)  # Apply Clipper to max track
    raw_max_mono, _ = audio_utils.preprocess_audio(raw_max_stereo, sr_raw, None)

    raw = clipper.process(raw, sr_raw)  # Apply Clipper to entire track

    loudness_max_after_clip = loudness.get_loudness(raw_max_stereo, sr_raw)
    print("loudness after clip", loudness_max_after_clip)

    loudness_after_clip = loudness.get_loudness(raw, sr_raw)
    print("loudness after clip", loudness_after_clip)

    print(np.max(raw))
    print(np.min(raw))

    # Save audio
    audio_utils.numpy_to_wav(raw_max_stereo, sr_raw, os.path.join("../tracks/edited", audiofile))
    audio_utils.numpy_to_wav(raw, sr_raw, os.path.join("../mastered", audiofile))

    # Load Back reference
    ref, sr_ref = audio_utils.load_audio_file("../tracks/reference_tracks/BreakTheFall.mp3")
    ref_max_mono, ref_max_stereo = audio_utils.preprocess_audio(ref, sr_ref, duration)

    # Loud raw track back
    raw, sr_raw = audio_utils.load_audio_file("../tracks/raw_tracks/" + audiofile)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)

    # Load back mastered track
    mastered, sr_mastered = audio_utils.load_audio_file("../mastered/" + audiofile)
    mastered_max_mono, mastered_max_stereo = audio_utils.preprocess_audio(mastered, sr_mastered, duration)

    #loudness of ref
    ref_loudness = loudness.get_loudness(ref_max_stereo, sr_ref)
    print("ref loudness", ref_loudness)

    # raw loudness
    raw_loudness = loudness.get_loudness(raw_max_stereo, sr_raw)
    print("raw loudness", raw_loudness)

    # mastered loudness
    mastered_loudness = loudness.get_loudness(mastered_max_stereo, sr_mastered)
    print("mastered loudness", mastered_loudness)


    # Create spectrums
    power_ref, freq = spectrum.create_spectrum(ref_max_mono, sr_ref)
    spec, freq = spectrum.create_spectrum(mastered_max_mono, sr_mastered)
    spec_raw, freq = spectrum.create_spectrum(raw_max_mono, sr_raw)

    plt.plot(freq, spec, label="mastered")
    #plt.plot(freq, spec_raw, label="raw")
    plt.plot(freq, power_ref, label="reference")
    plt.xscale('log')
    plt.legend()
    plt.show()


master("1.wav")

