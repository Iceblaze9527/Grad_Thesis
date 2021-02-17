import os
import time

import simpleaudio as simpad

root_path = '/home/pi'
wav_name = 'test.wav'

wav_path = os.path.join(root_path, wav_name)
wav_obj = simpad.WaveObject.from_wave_file(wav_path)

play_obj = wav_obj.play()
t = time.time()

# cyclic solution
while play_obj.is_playing():
    print("flag @ %e sec"%(time.time() - t))
    time.sleep(5)
play_obj.stop()

# one-shot solution
# time.sleep(5)
# print("flag @ %e sec"%(time.time() - t))
## play_obj.wait_done() #block mode enabled
# play_obj.stop()