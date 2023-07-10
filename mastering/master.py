from mastering.utils import audio_utils, loudness, spectrum
from mastering import constants, song_database
from mastering.plugins import custom_equalizer, custom_clipper
import os
import numpy as np


def master(audiofile):
    duration = constants.DURATION

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file("../uploads/" + audiofile)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)

    # Load database
    db = song_database.SpectrumDatabase()
    db.load_spectrum_database()

    specs = db.specs
    print("SHAPE SPECS", specs.shape)

    avg_spec = np.average(specs, axis=0)
    print("AVG_SPEC SHAPE", avg_spec.shape)
    raw_spec, freq = spectrum.create_spectrum(raw_max_mono, sr_raw)

    avg_raw = np.average(raw_spec)
    avg_ref = np.average(avg_spec)
    dif = avg_raw - avg_ref

    # Reference Spectrum Calculation
    power_ref = avg_spec + dif

    print(power_ref.shape)

    center_freqs = [(30, 100), (100, 250), (250, 500), (1000, 2000), (1500, 2500), (2000, 3000), (2500, 3500), (3000, 4000), (3500, 4500), (4000, 5000), (4500, 7500), (7500, 16000)]
    Q_values = [(0.1, 6) for _ in range(12)]
    gain = [(-16.0, 16.0) for _ in range(12)]
    bounds = gain + center_freqs + Q_values

    eq = custom_equalizer.CustomEqualizer()

    eq.find_set_settings(bounds, raw_max_mono, sr_raw, power_ref)
    raw_max_stereo = eq.process(raw_max_stereo, sr_raw)  # Apply Eq to entire track
    raw_max_mono, _ = audio_utils.preprocess_audio(raw_max_stereo, sr_raw, None)
    raw = eq.process(raw, sr_raw)  # Apply Eq to entire track

    # Clipper
    clipper = custom_clipper.CustomClipper()
    clipper.find_set_settings(raw_max_stereo, sr_raw, ref_loudness=constants.TARGET_LOUDNESS)

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
    audio_utils.numpy_to_wav(raw, sr_raw, os.path.join("../mastered", audiofile))

