from pybricks._common import Speaker

class Vocals:
    def __init__(self, speaker : Speaker, volume = 10):
        self.speaker : Speaker = speaker
        self.speaker.volume(volume)

    def beep_boop(self):
        self.speaker.beep(150, 50)
        self.speaker.beep(130, 50)

    def boop_beep(self):
        self.speaker.beep(120, 50)
        self.speaker.beep(140, 50)