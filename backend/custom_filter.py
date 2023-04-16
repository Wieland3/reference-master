from scipy.signal import butter, sosfilt


class CustomFilter:
    def __init__(self, lowcut, highcut, sr, gain):
        self.lowcut = lowcut
        self.highcut = highcut
        self.sr = sr
        self.gain = gain
        self.filter = butter(2, [self.lowcut, self.highcut], 'bandpass', fs=self.sr, output='sos')

    def set_params(self, values):
        self.lowcut = values[0]
        self.highcut = values[1]
        self.gain = values[2]
        self.filter = butter(2, [self.lowcut, self.highcut], 'bandpass', fs=self.sr, output='sos')

    def filter_audio(self, audio, gain=0):
        return sosfilt(self.filter, audio) * 10 ** (self.gain / 20)
