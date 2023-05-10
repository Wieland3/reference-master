import os
import numpy as np
from backend import index_embeddings
from backend import audio_utils
from backend import constants
from backend import loudness
from backend import spectrum
from backend import nova_eq
from backend import custom_clipper
from backend import mjuc
from backend import audio_features


def master(audiofile):
    duration = constants.DURATION

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file("../uploads/" + audiofile)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)

    # Find the closest reference track
    embeddings = index_embeddings.IndexEmbeddings(38)
    closest_track = embeddings.find_closest(raw_max_mono,sr_raw ,1)
    print(closest_track)

    # Load closest reference track
    ref, sr_ref = audio_utils.load_audio_file(closest_track[0])
    ref_max_mono, ref_max_stereo = audio_utils.preprocess_audio(ref, sr_ref, duration)

    # Loudness Calculation
    raw_loudness = loudness.get_loudness(raw_max_stereo, sr_raw)
    ref_loudness = loudness.get_loudness(ref_max_stereo, sr_ref)

    ref_max_loudness_adjusted_stereo = loudness.equal_loudness(ref_max_stereo, sr_ref, raw_loudness)
    ref_max_mono, _ = audio_utils.preprocess_audio(ref_max_loudness_adjusted_stereo, sr_ref, None)

    # Calculate Crest Factor
    crest_ref = audio_features.crest_factor(ref_max_mono)
    crest_raw = audio_features.crest_factor(raw_max_mono)

    # Reference Spectrum Calculation
    power_ref = spectrum.create_spectrum(ref_max_mono, sr_ref)

    # MJUC
    comp = mjuc.MJUC(constants.PATH_TO_MJUC)
    comp.find_set_settings(raw_max_stereo, sr_raw)
    raw_max_stereo = comp.process(raw_max_stereo, sr_raw)
    raw_max_mono, _ = audio_utils.preprocess_audio(raw_max_stereo, sr_raw, None)
    raw = comp.process(raw, sr_raw) # Apply Compressor to entire track

    # Nova Eq
    low_bounds = [(-17,17), (0.1,6), (30,100)]
    low_mid_bounds = [(-17,17), (0.1,6), (100, 1000)]
    high_mid_bounds = [(-17,17), (0.1,6), (1000, 7500)]
    high_bounds = [(-17,17), (0.1,6), (7500, 20000)]
    bounds = low_bounds + low_mid_bounds + high_mid_bounds + high_bounds

    eq = nova_eq.NovaEq(constants.PATH_TO_NOVA_PLUGIN, "High S")

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
    audio_utils.numpy_to_wav(raw, sr_raw, os.path.join("../mastered", audiofile))
