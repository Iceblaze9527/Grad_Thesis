class Sounds():
    def __init__(self):
        pass


def play_audio(obj):
    return obj.play()

def stop_audio(obj):
    obj.stop()

# if __name__ == '__main__':
#     wav_path = os.path.join(root_path, wav_name)
#     wav_obj = simpad.WaveObject.from_wave_file(wav_path)
#     play_obj = play_audio(wav_obj)
#     print('non-blocking is great')
#     time.sleep(1.5)
#     stop_audio(play_obj)