import pygame as pg
from util.get_files_is_type import files_is_type
import random

class SoundEffects:
    def __init__(self, file_dir):
        if pg.mixer.get_init() is None:
            pg.mixer.init()
        sound_files_list = files_is_type(file_dir=file_dir, file_type='.mp3')
        self.sound_list = []
        for sound_file in sound_files_list:
            sound = pg.mixer.Sound(sound_file)
            sound .set_volume(1.0)
            self.sound_list.append(sound)
    
    def play(self):
        random.choice(self.sound_list).play()

hit_sound_effects = SoundEffects('assets/sound/hit_sound/')
swing_sound_effects = SoundEffects('assets/sound/swing_sound/')