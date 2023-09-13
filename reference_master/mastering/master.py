from reference_master.utils import audio_utils, loudness, spectrum
from reference_master import constants
from reference_master.plugins.equalizer import Equalizer
from reference_master.plugins.clipper import Clipper
import os


def master(raw_track, ref_track, target_loudness=None):
    """
    Masters a raw track based on a reference track and saves to songs/mastered folder.
    :param raw_track: name of raw track
    :param ref_track: name of reference track
    :param target_loudness: target loudness of mastered track. If not given, loudness of reference track is used.
    :return: None
    """
    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file(constants.PATH_TO_RAW_SONGS + raw_track)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, constants.DURATION)

    # Load reference track
    ref, sr_ref = audio_utils.load_audio_file(constants.PATH_TO_REFERENCE_SONGS + ref_track)
    ref_max_mono, ref_max_stereo = audio_utils.preprocess_audio(ref, sr_ref, constants.DURATION)

    # Loudness Calculation
    raw_loudness = loudness.get_loudness(raw_max_stereo, sr_raw)

    # Select if target loudness should be calculated based on reference track or given as parameter
    if target_loudness is None:
        target_loudness = loudness.get_loudness(ref_max_stereo, sr_ref)

    # Equalize Loudness
    ref_max_loudness_adjusted_stereo = loudness.equal_loudness(ref_max_stereo, sr_ref, raw_loudness)
    ref_max_mono, _ = audio_utils.preprocess_audio(ref_max_loudness_adjusted_stereo, sr_ref, None)

    # Reference Spectrum Calculation
    power_ref, power_freq = spectrum.create_spectrum(ref_max_mono, sr_ref)

    # Settings for equalizer
    center_freqs = [(30, 100), (100, 250), (250, 500), (1000, 2000), (1500, 2500), (2000, 3000), (2500, 3500), (3000, 4000), (3500, 4500), (4000, 5000), (4500, 7500), (7500, 16000)]
    Q_values = [(0.1, 6) for _ in range(12)]
    gain = [(-16.0, 16.0) for _ in range(12)]
    bounds = gain + center_freqs + Q_values

    eq = Equalizer()

    # Find best settings for equalizer
    eq.find_set_settings(bounds, raw_max_mono, sr_raw, power_ref)

    # Apply Eq to max track
    raw_max_stereo = eq.process(raw_max_stereo, sr_raw)
    raw_max_mono, _ = audio_utils.preprocess_audio(raw_max_stereo, sr_raw, None)

    # Apply Eq to entire track
    raw = eq.process(raw, sr_raw)

    # Clipper
    clipper = Clipper()
    clipper.find_set_settings(raw_max_stereo, sr_raw, ref_loudness=target_loudness)

    # Apply Clipper to entire track
    raw = clipper.process(raw, sr_raw)

    # Save audio
    audio_utils.numpy_to_wav(raw, sr_raw, os.path.join(constants.PATH_TO_MASTERED_SONGS, raw_track))
