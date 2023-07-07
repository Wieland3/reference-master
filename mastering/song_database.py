from mastering import constants
from mastering.utils import audio_distance, audio_utils, loudness, spectrum
import numpy as np
import glob


class SpectrumDatabase:
    def __init__(self):
        self.audio = None
        self.sr = None
        self.specs = None
        self.freqs = None

    def create_spectrum_database(self, loudness_norm=constants.LOUDNESS_NORM):
        """
        Creates a npz file of all the songs in the reference folder.
        :return:
        """
        audio_db = []
        specs_db = []
        sr_db = []
        freqs = []
        for i, filepath in enumerate(glob.iglob('../tracks/reference_tracks/*.mp3')):
            audio, sr = audio_utils.load_audio_file(filepath)
            _, audio_max_stereo = audio_utils.preprocess_audio(audio, sr, constants.DURATION)
            audio_max_stereo = loudness.equal_loudness(audio_max_stereo, sr, loudness_norm)
            audio_max_mono, _ = audio_utils.preprocess_audio(audio_max_stereo, sr, None)
            spec, freq = spectrum.create_spectrum(audio_max_mono, sr)
            audio_db.append(audio_max_stereo)
            sr_db.append(sr)
            specs_db.append(spec)
            freqs.append(freq)
        audio_db = np.array(audio_db)
        sr_db = np.array(sr_db)
        specs = np.array(specs_db)
        freqs = np.array(freqs)
        np.savez('../spectrum_database/db.npz', specs=specs, freqs=freqs, audio=audio_db, sr=sr_db)
        self.audio = audio_db
        self.sr = sr_db
        self.specs = specs
        self.freqs = freqs

    def load_spectrum_database(self):
        """
        Loads the npz file of all the songs in the reference folder.
        :return:
        """
        db = np.load('../spectrum_database/db.npz')
        self.audio = db['audio']
        self.sr = db['sr']
        self.specs = db['specs']
        self.freqs = db['freqs']

    def find_closest(self, audio, sr):
        """
        Finds the n_closest reference tracks to the audio file at path_to_audio
        :param audio: audio to find closest spec for
        :param sr: sr of that audio
        :return: spectrum of closest tracks
        """
        closest_index = None
        closest_dist = np.inf
        for i in range(self.specs.shape[0]):
            dist = audio_distance.song_distance(audio, sr, self.specs[i])
            print(dist)
            if dist < closest_dist:
                closest_dist = dist
                closest_index = i
        return closest_index


"""
db = SpectrumDatabase()
db.create_spectrum_database()
db.load_spectrum_database()

raw, sr = audio_utils.load_audio_file('../tracks/raw_tracks/2.wav')
audio, _ = audio_utils.preprocess_audio(raw, sr, constants.DURATION)
audio = loudness.equal_loudness(audio, sr, -12.0)
spec_audio = spectrum.create_spectrum(audio, sr)
closest_index = db.find_closest(audio, sr)

closest = db.specs[closest_index]

print(audio_distance.song_distance(audio, sr, closest))
"""