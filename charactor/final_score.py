from pandas import wide_to_long
import pygame as pg
from util.color import Color

width, height = 1920, 1010                      #遊戲畫面寬和高

class BackButton(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pg.image.load('assets/back_button.png')
        self.rect = self.image.get_rect()
        self.rect.center = (width/2 + 195, height/2 - 157)
    
    # def update(self) -> None:
    #     pass

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y)) 

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False


class FinalScoreBoard(pg.sprite.Sprite):
    def __init__(self, score:int = 0):
        super().__init__()
        self.score = score
        self.image = pg.image.load('assets/final_score_board.png')
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        self.font_l1 = pg.font.SysFont('microsoftyaheiui', 48)
        self.font_l2 = pg.font.Font("assets/fonts/monogram/ttf/monogram.ttf", 64)
        # l for line, line1 line2

    def update(self):
        self.text_l1 = self.font_l1.render('得分 :', True, Color.BLACK)
        self.text_l2 = self.font_l2.render(str(self.score), True, Color.BLACK)
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text_l1, (self.rect.x + 100, self.rect.y + 120))
        screen.blit(self.text_l2, (self.rect.x + 100, self.rect.y + 230))


class FinalGradeBoard(pg.sprite.Sprite):
    def __init__(self, score:float = 0):
        super().__init__()
        self.score = score
        self.image = pg.image.load('assets/final_score_board.png')
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        self.font_l1 = pg.font.SysFont('microsoftyaheiui', 36)
        self.font_l2 = pg.font.Font("assets/fonts/monogram/ttf/monogram.ttf", 64)
        # l for line, line1 line2

    def update(self):
        self.text_l1 = self.font_l1.render('平均相似度 :', True, Color.BLACK)
        self.text_l2 = self.font_l2.render(str(self.score), True, Color.BLACK)
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(self.text_l1, (self.rect.x + 100, self.rect.y + 120))
        screen.blit(self.text_l2, (self.rect.x + 100, self.rect.y + 230))