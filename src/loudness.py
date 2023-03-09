import pyloudnorm


def get_loudness(audio, sr):
    # this function should calculate the loudness of a song
    # the song is a numpy array
    # the sample rate is an integer
    # return the loudness
    meter = pyloudnorm.Meter(sr)
    loudness = meter.integrated_loudness(audio)
    return loudness


def equal_loudness(audio, sr, target_loudness):
    # this function should change the loudness of a song to a target loudness
    # the song is a numpy array
    # the sample rate is an integer
    # the target loudness is a float
    # return the new audio
    meter = pyloudnorm.Meter(sr)
    loudness = meter.integrated_loudness(audio)
    audio = pyloudnorm.normalize.loudness(audio, loudness, target_loudness)
    return audio
