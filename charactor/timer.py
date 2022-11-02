import pygame as pg
from util.color import Color

width = 1280 # should import from main.py but I don't know how to import

class Timer(pg.sprite.Sprite):
    def __init__(self, remain_time:int):
        super().__init__()
        self.remain_time = remain_time
        self.image = pg.image.load('assets/scoreboard.bmp')
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, self.rect.height/2)
        # self.font = pg.font.SysFont('Arial', 30)
        self.font = pg.font.Font("assets/fonts/monogram/ttf/monogram.ttf", 48)
        self.text = self.font.render(str(self.remain_time), True, Color.BLACK)

    def set_remain_time(self, remain_time):
        self.remain_time = int(remain_time)

    def update(self):
        self.text = self.font.render(str(self.remain_time), True, Color.BLACK)
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text, (self.rect.x + 20, self.rect.y + 20))
