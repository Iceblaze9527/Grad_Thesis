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

# if __name__ == '__main__':
#     wav_path = os.path.join(root_path, wav_name)
#     wav_obj = simpad.WaveObject.from_wave_file(wav_path)
#     play_obj = play_audio(wav_obj)
#     print('non-blocking is great')
#     time.sleep(1.5)
#     stop_audio(play_obj)