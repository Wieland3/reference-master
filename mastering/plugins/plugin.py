import pedalboard


class Plugin:
    def __init__(self):
        self.board = None

    def set_params(self, values):
        pass

    def process(self, audio, sr):
        return self.board(audio, sr)

