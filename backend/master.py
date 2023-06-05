import os
import numpy as np
import matplotlib.pyplot as plt
from backend import index_embeddings
from backend import audio_utils
from backend import constants
from backend import loudness
from backend import spectrum
from backend import custom_clipper
from backend import custom_eq


def master(audiofile):
    duration = constants.DURATION
    path = "../tracks/raw_tracks/" + audiofile

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file("../uploads/" + path)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)

    # Find the closest reference track
    embeddings = index_embeddings.IndexEmbeddings(38)
    closest_track = embeddings.find_closest(raw_max_mono,sr_raw, 1)
    print(closest_track)

    # Load closest reference track
    ref, sr_ref = audio_utils.load_audio_file(closest_track[0])
    ref_max_mono, ref_max_stereo = audio_utils.preprocess_audio(ref, sr_ref, duration)

    # Loudness Calculation
    raw_loudness = loudness.get_loudness(raw_max_stereo, sr_raw)
    ref_loudness = loudness.get_loudness(ref_max_stereo, sr_ref)

    ref_max_loudness_adjusted_stereo = loudness.equal_loudness(ref_max_stereo, sr_ref, raw_loudness)
    ref_max_mono, _ = audio_utils.preprocess_audio(ref_max_loudness_adjusted_stereo, sr_ref, None)

    # Reference Spectrum Calculation
    power_ref, freq = spectrum.create_spectrum(ref_max_mono, sr_ref)

    # Custom Eq
    low_bounds = [(30, 500), (1, 10), (-16, 16)]
    #low_mid_bounds = [(100, 250), (0.1, 10), (-12, 12)]
    mid_bounds = [(500, 7500), (1, 10), (-16, 16)]
    #high_mid_bounds = [(500, 1000), (0.1, 10), (-12, 12)]
    high_bounds = [(7500, 20000), (1, 10), (-16, 16)]

    bounds = low_bounds + mid_bounds + high_bounds

    eq = custom_eq.CustomEq()

    eq.find_set_settings(bounds, raw_max_mono, sr_raw, power_ref, mode='direct')
    raw_max_stereo = eq.process(raw_max_stereo, sr_raw)
    raw_max_mono, _ = audio_utils.preprocess_audio(raw_max_stereo, sr_raw, None)
    raw = eq.process(raw, sr_raw)  # Apply Eq to entire track

    print("max before clip", np.max(raw))
    print("min before clip", np.min(raw))
    # Clipper
    clipper = custom_clipper.CustomClipper()
    clipper.find_set_settings(raw_max_stereo, sr_raw, mode='loudness', ref_loudness=-7)

    raw = clipper.process(raw, sr_raw)  # Apply Clipper to entire track

    print(np.max(raw))
    print(np.min(raw))

    # Save audio
    audio_utils.numpy_to_wav(raw_max_stereo, sr_raw, os.path.join("../tracks/edited", audiofile))
    audio_utils.numpy_to_wav(raw, sr_raw, os.path.join("../mastered", audiofile))


    # Load Back audio and plot spectrums
    ref, sr_ref = audio_utils.load_audio_file(closest_track[0])
    ref_max_mono, ref_max_stereo = audio_utils.preprocess_audio(ref, sr_ref, duration)
    power_ref, freq = spectrum.create_spectrum(ref_max_mono, sr_ref)
    raw, sr_raw = audio_utils.load_audio_file("../mastered/" + audiofile)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)
    spec, freq = spectrum.create_spectrum(raw_max_mono, sr_raw)
    plt.plot(freq, spec, label="mastered")
    plt.plot(freq, power_ref, label="reference")
    plt.xscale('log')
    plt.legend()
    plt.show()


master("4.wav")

