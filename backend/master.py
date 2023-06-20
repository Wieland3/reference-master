from backend import index_embeddings
from backend import audio_utils
from backend import constants
from backend import loudness
from backend import spectrum
from backend import custom_clipper
from backend import equalizer
import os
import numpy as np
import matplotlib.pyplot as plt


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

    center_freqs = [(30.0, 100.0), (100.0, 500.0), (500.0, 7500.0), (7500.0, 16000.0)]
    Q_values = [(0.1, 6.0) for _ in range(4)]
    gain = [(-12.0, 12.0) for _ in range(4)]
    bounds = center_freqs + Q_values + gain

    print("Bounds", bounds)
    print("LEN", len(bounds))
    eq = equalizer.Equalizer(sr_raw)

    eq.find_set_settings(bounds, raw_max_mono, sr_raw, power_ref, mode='direct')
    raw_max_stereo = eq.process(raw_max_stereo)
    raw_max_mono, _ = audio_utils.preprocess_audio(raw_max_stereo, sr_raw, None)
    raw = eq.process(raw)  # Apply Eq to entire track

    print("max before clip", np.max(raw))
    print("min before clip", np.min(raw))
    # Clipper
    clipper = custom_clipper.CustomClipper()
    clipper.find_set_settings(raw_max_stereo, sr_raw, mode='loudness', ref_loudness=ref_loudness)

    raw = clipper.process(raw, sr_raw)  # Apply Clipper to entire track

    print(np.max(raw))
    print(np.min(raw))

    # Save audio
    audio_utils.numpy_to_wav(raw_max_stereo, sr_raw, os.path.join("../tracks/edited", audiofile))
    audio_utils.numpy_to_wav(raw, sr_raw, os.path.join("../mastered", audiofile))


    # Load Back audio and plot spectrums
    ref, sr_ref = audio_utils.load_audio_file(closest_track[0])
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


master("12.wav")

