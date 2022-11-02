import random
from typing import Tuple
import pygame as pg
import time
import numpy as np
from util.color import Color
from util.sound_effects import hit_sound_effects

height = 720 # should import from main.py but I don't know how to import
GRAVITY = 9.8/5 # 9.8/6 #
MAX_FALL_SPEED = 9.8*2#1#3
SIZE_INC_RATE = 50 #100 #50
SIZE_DEC_RATE = 3
DISPLAY_OUTER_CIRLE_RATE = 0.8
MIN_SIZE = 20

class Shuttlecock(pg.sprite.Sprite):
    def __init__(self, start_pos:Tuple[int,int], special_judge=False):
        super().__init__()
        self.rot_deg = -45
        self.size = 50
        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load('assets/shuttlecock.png'), (self.size , self.size)) , self.rot_deg)
        self.image_ori = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = start_pos

        self.special_judge = special_judge
        
        self.speed = pg.math.Vector2(0, 0)
        self.accel = pg.math.Vector2(0, GRAVITY)
        
        self.speedx_postive = True if self.speed.x > 0 else False

        self.init_time = time.perf_counter()
        self.now_time = 0.0
        self.can_hit = False
        self.can_hit_after_throw = random.uniform(0.5, 1.2)

        self.score = 1

        self.far_to_close = True
        self.hit_time = 0.0

    def set_start_pos(self, pos:Tuple[int,int]):    
        self.rect.center = pos

    def set_speed(self, speed:pg.math.Vector2):
        if type(speed) == tuple:
            speed = pg.math.Vector2(speed)
        self.speed = speed
    
    def set_accel(self, accel:pg.math.Vector2):
        if type(accel) == tuple:
            accel = pg.math.Vector2(accel)
        self.accel = accel

    def set_can_hit_after_throw(self, time):
        self.can_hit_after_throw = time
    

    def set_far_to_close(self, flag):
        self.far_to_close = flag
        self.can_hit = False
        if flag is False:
            self.play_hit_sound()
            self.speed.x = - self.speed.x
            self.speed.y = -20
            self.init_time = self.now_time

    def handle_speed(self):
        self.speed.y = min((self.now_time - self.init_time) * self.accel.y + self.speed.y, MAX_FALL_SPEED)
        self.speed.x = (self.now_time - self.init_time) * self.accel.x + self.speed.x
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

    def handle_rotate(self):
        if self.far_to_close:
            self.size = 50 + (self.now_time - self.init_time) * SIZE_INC_RATE
        else: 
            self.size = max(self.size - (self.now_time - self.init_time) * SIZE_DEC_RATE, MIN_SIZE)
        self.rot_deg = np.arctan2(self.speed.x, self.speed.y) * 180 / np.pi +180.0
        self.image = pg.transform.scale(pg.transform.rotate(self.image_ori, self.rot_deg), (self.size , self.size))


    def handle_hit(self):
        if self.far_to_close is False :
            self.can_hit = False
        elif not self.special_judge and ( ( self.now_time - self.init_time >= self.can_hit_after_throw ) or (self.rect.y > height*2/3) ):
        # elif not self.special_judge and ( ( self.now_time - self.init_time >= self.can_hit_after_throw ) ):
            self.can_hit = True
        elif self.special_judge:
            if self.now_time-self.init_time - self.can_hit_after_throw <= 0:
                pass 
            elif self.now_time-self.init_time - self.can_hit_after_throw <= DISPLAY_OUTER_CIRLE_RATE :
                self.can_hit = True
                self.score = int( np.sin((self.now_time - self.init_time - self.can_hit_after_throw)/DISPLAY_OUTER_CIRLE_RATE * np.pi / 2 ) * 1100 )
            elif self.now_time-self.init_time - self.can_hit_after_throw <= 1.2:
                self.can_hit = True
                self.score = int( 1000 + random.randint(-100, 100) )

                


    def update(self):
        self.now_time = time.perf_counter()
        self.handle_speed()
        self.handle_rotate()
        self.handle_hit()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x-self.size/2, self.rect.y-self.size/2))
        if self.far_to_close:
            if self.special_judge:
                pg.draw.circle(screen, Color.LIGHT_GRAY, (self.rect.x, self.rect.y), 120/3, 3)
                if self.now_time-self.init_time - self.can_hit_after_throw <= 0:
                    pass 
                elif self.now_time-self.init_time - self.can_hit_after_throw <= DISPLAY_OUTER_CIRLE_RATE :
                    pg.draw.circle(screen, Color.DARK_GRAY, (self.rect.x, self.rect.y), (1- np.sin((self.now_time - self.init_time - self.can_hit_after_throw)/DISPLAY_OUTER_CIRLE_RATE * np.pi / 2 ) ) * 50 + 120/3, 4)
                elif self.now_time-self.init_time - self.can_hit_after_throw <= 1.2:
                    pg.draw.circle(screen, Color.RED, (self.rect.x, self.rect.y), 120/3, 5)
            elif self.can_hit :
                pg.draw.circle(screen, Color.GREEN, (self.rect.x, self.rect.y), self.size/3, 3)

    def play_hit_sound(self):
        hit_sound_effects.play()

