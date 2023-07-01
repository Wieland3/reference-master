from backend import index_embeddings
from backend import audio_utils
from backend import constants
from backend import loudness
from backend import spectrum
from backend import custom_clipper
from backend import custom_equalizer
from backend import song_database
import os
import numpy as np
import matplotlib.pyplot as plt


def master(audiofile):
    duration = constants.DURATION
    path = "../tracks/raw_tracks/" + audiofile

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file("../uploads/" + path)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)

    # Bring the raw track to the same loudness as the reference tracks
    raw_max_loudness_adjusted_stereo = loudness.equal_loudness(raw_max_stereo, sr_raw, constants.LOUDNESS_NORM)
    raw_max_loudness_adjusted_mono, _ = audio_utils.preprocess_audio(raw_max_loudness_adjusted_stereo, sr_raw, None)

    # Find the closest reference track
    db = song_database.SpectrumDatabase()
    db.load_spectrum_database()
    closest_track = db.find_closest(raw_max_loudness_adjusted_mono, sr_raw)

    # Load closest reference track
    ref, sr_ref = db.audio[closest_track], db.sr[closest_track]
    ref_max_mono, ref_max_stereo = audio_utils.preprocess_audio(ref, sr_ref, None)

    # Loudness Calculation
    raw_loudness = loudness.get_loudness(raw_max_stereo, sr_raw)

    # Make sure the reference track is the same loudness as the raw track
    ref_max_loudness_adjusted_stereo = loudness.equal_loudness(ref_max_stereo, sr_ref, raw_loudness)
    ref_max_mono, _ = audio_utils.preprocess_audio(ref_max_loudness_adjusted_stereo, sr_ref, None)

    # Reference Spectrum Calculation
    power_ref, freq = spectrum.create_spectrum(ref_max_mono, sr_ref)

    center_freqs = [(30.0, 150.0), (150.0, 500.0), (500.0, 1000.0), (1000.0, 7500.0), (7500.0, 16000.0)]
    Q_values = [(0.01, 12.0) for _ in range(5)]
    gain = [(-16.0, 16.0) for _ in range(5)]
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
    clipper.find_set_settings(raw_max_stereo, sr_raw, mode='loudness', ref_loudness=constants.LOUDNESS)

    raw = clipper.process(raw, sr_raw)  # Apply Clipper to entire track

    print(np.max(raw))
    print(np.min(raw))

    # Save audio
    audio_utils.numpy_to_wav(raw_max_stereo, sr_raw, os.path.join("../tracks/edited", audiofile))
    audio_utils.numpy_to_wav(raw, sr_raw, os.path.join("../mastered", audiofile))


    # Load Back audio and plot spectrums
    ref_max_mono, ref_max_stereo = audio_utils.preprocess_audio(ref, sr_ref, duration)

    #loudness of ref
    ref_loudness = loudness.get_loudness(ref_max_stereo, sr_ref)
    print("ref loudness", ref_loudness)
    # loudness of mastered

    power_ref, freq = spectrum.create_spectrum(ref_max_mono, sr_ref)
    raw, sr_raw = audio_utils.load_audio_file("../mastered/" + audiofile)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)

    raw_loudness = loudness.get_loudness(raw_max_stereo, sr_raw)
    print("raw loudness", raw_loudness)

    spec, freq = spectrum.create_spectrum(raw_max_mono, sr_raw)
    plt.plot(freq, spec, label="mastered")
    plt.plot(freq, power_ref, label="reference")
    plt.xscale('log')
    plt.legend()
    plt.show()


master("7.wav")

