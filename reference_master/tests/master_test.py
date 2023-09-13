from reference_master.utils import audio_utils, loudness, spectrum
from reference_master import constants, song_database
from reference_master.plugins import custom_equalizer, custom_clipper, custom_compressor, custom_saturator
import os
import numpy as np
import matplotlib.pyplot as plt


def master(audiofile):
    duration = constants.DURATION
    path = "../../tracks/raw_tracks/" + audiofile

    # Load raw track
    raw, sr_raw = audio_utils.load_audio_file(path)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)

    # Load database
    db = song_database.SpectrumDatabase()
    db.load_spectrum_database(path_to_db='../../spectrum_database/db.npz')

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

    plt.plot(raw_spec, label="raw")
    plt.plot(power_ref, label="ref")
    plt.legend()
    plt.show()

    kernel_size = 20
    kernel = np.ones(kernel_size) / kernel_size

    dif_ref = np.convolve(np.diff(power_ref), kernel, mode='valid')
    dif_raw = np.convolve(np.diff(raw_spec), kernel, mode='valid')

    plt.plot(dif_raw, label="raw")
    plt.plot(dif_ref, label="ref")
    plt.legend()
    plt.show()


    center_freqs = [(30, 100), (100, 250), (250, 500), (1000, 2000), (1500, 2500), (2000, 3000), (2500, 3500), (3000, 4000), (3500, 4500), (4000, 5000), (4500, 7500), (7500, 16000)]
    Q_values = [(0.1, 6) for _ in range(12)]
    gain = [(-16.0, 16.0) for _ in range(12)]
    bounds = gain + center_freqs + Q_values

    eq = custom_equalizer.CustomEqualizer()

    eq.find_set_settings(bounds, raw_max_mono, sr_raw, power_ref)
    #eq.set_params([7.9, -6.5, 1.6, -15.6, 12.4, 6.8, -7.8, 12.6, -6.2, 3.7, 6.2, 5.1, 30.8, 165.3, 420.7, 1565.4, 1523.1, 2001.9, 3164.9, 3113.1, 3980.3, 4468.3, 7465.1, 9268.1, 1.7, 4.4, 5.3, 0.9, 4.4, 3.6, 4.0, 4.6, 1.2, 1.8, 0.2, 1.7])
    raw_max_stereo = eq.process(raw_max_stereo, sr_raw)  # Apply Eq to entire track
    raw_max_mono, _ = audio_utils.preprocess_audio(raw_max_stereo, sr_raw, None)
    raw = eq.process(raw, sr_raw)  # Apply Eq to entire track

    print("max before clip", np.max(raw))
    print("min before clip", np.min(raw))
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
    audio_utils.numpy_to_wav(raw_max_stereo, sr_raw, os.path.join("../../tracks/edited", audiofile))
    audio_utils.numpy_to_wav(raw, sr_raw, os.path.join("../../mastered", audiofile))

    # Loud raw track back
    raw, sr_raw = audio_utils.load_audio_file("../../tracks/raw_tracks/" + audiofile)
    raw_max_mono, raw_max_stereo = audio_utils.preprocess_audio(raw, sr_raw, duration)

    # Load back mastered track
    mastered, sr_mastered = audio_utils.load_audio_file("../../mastered/" + audiofile)
    mastered_max_mono, mastered_max_stereo = audio_utils.preprocess_audio(mastered, sr_mastered, duration)

    # raw loudness
    raw_loudness = loudness.get_loudness(raw_max_stereo, sr_raw)
    print("raw loudness", raw_loudness)

    # mastered loudness
    mastered_loudness = loudness.get_loudness(mastered_max_stereo, sr_mastered)
    print("mastered loudness", mastered_loudness)

    spec, freq = spectrum.create_spectrum(mastered_max_mono, sr_mastered)
    spec_raw, freq = spectrum.create_spectrum(raw_max_mono, sr_raw)

    avg_mastered = np.average(spec)
    avg_ref = np.average(avg_spec)
    dif = avg_mastered - avg_ref

    # Reference Spectrum Calculation
    power_ref = avg_spec + dif

    plt.plot(freq, spec, label="mastered")
    #plt.plot(freq, spec_raw, label="raw")
    plt.plot(freq, power_ref, label="reference")
    plt.xscale('log')
    plt.legend()
    plt.show()

    dif_ref = np.convolve(np.diff(power_ref), kernel, mode='valid')
    dif_raw = np.convolve(np.diff(spec), kernel, mode='valid')

    plt.plot(dif_raw, label="raw")
    plt.plot(dif_ref, label="ref")
    plt.legend()
    plt.show()

master("KLK 29 (MIX).wav")
