import sys 
sys.path.append("..") 

from ctrl.led import LEDEyes
from ctrl.sound import SoundPlay

from param import OUTPUT_PAR

class OutputDevices():
    def __init__(self):
        self.led = LEDEyes(OUTPUT_PAR['period'], *list(OUTPUT_PAR['led'].values()))

    def exec_action(self, action):
        sound = SoundPlay(OUTPUT_PAR['wav_path'], OUTPUT_PAR['wav_files'][action])
        sound.play()
        
        if OUTPUT_PAR['action_space'][action] == 'HAP_LOOK':
            (self.led).happy_eyes(50, 2, 128)
        elif OUTPUT_PAR['action_space'][action] == 'SAD_LOOK':
            (self.led).sad_eyes(50, 192)
        elif OUTPUT_PAR['action_space'][action] == 'FEA_LOOK':
            (self.led).fear_eyes(25, 192, 1)
        elif OUTPUT_PAR['action_space'][action] == 'ANG_LOOK':
            (self.led).angry_eyes(25, 192)
        elif action == -2:
            (self.led).success_eyes()
        elif action == -1:
            (self.led).fail_eyes()

        sound.stop()
    
    def closeall(self):
        (self.led.strip)._cleanup()