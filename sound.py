import os
import simpleaudio as simpad

class SoundPlay():
    def __init__(self, path, wav_name):
        wav_path = os.path.join(path, wav_name)
        self.wav_obj = simpad.WaveObject.from_wave_file(wav_path)

    def play(self):
        self.play_obj = (self.wav_obj).play()

    def stop(self):
        (self.play_obj).stop()