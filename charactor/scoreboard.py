import pygame as pg
from util.color import Color

class ScoreBoard(pg.sprite.Sprite):
    def __init__(self, score:int = 0):
        super().__init__()
        self.score = score
        self.image = pg.image.load('assets/scoreboard.bmp')
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.font = pg.font.Font("assets/fonts/monogram/ttf/monogram.ttf", 48)
        
        self.text = self.font.render(str(self.score), True, Color.BLACK)

    def update(self):
        self.text = self.font.render(str(self.score), True, Color.BLACK)
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text, (self.rect.x + 20, self.rect.y + 20))

class SimilarityBoard(pg.sprite.Sprite):
    def __init__(self, score:float = 0):
        super().__init__()
        self.score = score
        self.image = pg.image.load('assets/scoreboard.bmp')
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.font = pg.font.Font("assets/fonts/monogram/ttf/monogram.ttf", 36)

    def update(self):
        self.text_l1 = self.font.render("Similarity:", True, Color.BLACK)
        self.text_l2 = self.font.render(str(self.score), True, Color.BLACK)
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text_l1, (self.rect.x + 20, self.rect.y + 20))
        screen.blit(self.text_l2, (self.rect.x + 20, self.rect.y+35 + 20))
