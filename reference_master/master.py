from reference_master.utils import audio_utils, loudness, spectrum
from reference_master import constants
from reference_master.plugins import custom_equalizer, custom_clipper
import os
import numpy as np


def master(raw_track, ref_track):
    duration = constants.DURATION

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file("../songs/raw/" + raw_track)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)

    # Load reference track
    ref, sr_ref = audio_utils.load_audio_file("../songs/references/" + ref_track)
    ref_max_mono, ref_max_stereo = audio_utils.preprocess_audio(ref, sr_ref, duration)

    # Reference Spectrum Calculation
    power_ref, power_freq = spectrum.create_spectrum(ref_max_mono, sr_ref)

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
    audio_utils.numpy_to_wav(raw, sr_raw, os.path.join("../songs/mastered", raw_track))

master("raw_0.wav", "11 - Circle With Me.mp3")

