from scipy.signal import butter, sosfilt


class CustomFilter:
    def __init__(self, lowcut, highcut, sr, gain=0):
        self.gain = 10 ** (gain / 20)
        self.filter = butter(2, [lowcut, highcut], 'bandpass', fs=sr, output='sos')

    def set_gain(self, gain):
        self.gain = gain

    def filter_audio(self, audio):
        return sosfilt(self.filter, audio) * self.gain
