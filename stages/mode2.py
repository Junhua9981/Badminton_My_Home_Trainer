from typing import Tuple
import pygame as pg
import random
import argparse
import cv2
import numpy as np
import time
from objectDetectionModule import ObjectDetection
from charactor.shuttlecock import Shuttlecock
from charactor.scoreboard import ScoreBoard
from charactor.timer import Timer
from util.color import Color

width, height = 1280, 720                      #遊戲畫面寬和高
hit_size = 0.5 #接觸方框縮放

# def draw_detections(results, screen):
#         """
#         It takes the results of the detection and draws the bounding boxes on the screen
        
#         :param results: the output of the detection function
#         :param screen: the screen to draw on
#         """
#         labels, cord = results
#         n = len(labels)
#         x_shape, y_shape = width , height
#         for i in range(n):
#             row = cord[i]
#             if row[4] >= 0.2 :
#                 x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
#                 pg.draw.rect(screen, (255, 0, 0), pg.Rect(x1, y1, x2-x1, y2-y1), 2)
                
#                 screen.blit(font.render(detection.class_to_label(labels[i]), True, (255, 0, 0)), (x1, y1))

def filter_detections(results):
    """
    It takes the results of the detection and filters the results based on the confidence
    
    :param results: the output of the detection function
    :return: the filtered results
    """
    labels, cord = results
    n = len(labels)
    filtered_results = []
    for i in range(n):
        row = cord[i]
        if row[4] >= 0.42 :
            filtered_results.append(row)
    return filtered_results

def get_collision_detections(filtered_results):
    collision_boxes = []
    for row in filtered_results:
        x1, y1, x2, y2 = int(row[0]*width), int(row[1]*height), int(row[2]*width), int(row[3]*height)
        col_width, col_height = (x2-x1)*hit_size, (y2-y1)*hit_size
        col_x, col_y = x1 + (x2-x1)/2 - col_width/2, y1 + (y2-y1)/2 - col_height/2
        collision_boxes.append((col_x, col_y, col_width, col_height))
    return collision_boxes

def initail_new_shuttlecock(start_pos: Tuple[int, int], speed: Tuple[int, int]):
    if start_pos is Tuple:
        new_shuttlecock = Shuttlecock(start_pos)
    elif start_pos is None:
        new_shuttlecock = Shuttlecock((random.randint(width*2/5, width*3/5) , height/3))
    if speed is Tuple:
        new_shuttlecock.set_speed( speed )
    elif speed is None:
        new_shuttlecock.set_speed(
            pg.math.Vector2( random.randint(-5, 5), random.randint(-20, -5) )
            )
    return new_shuttlecock

def stage2(cap, detection):

    # 初始化pygame
    pg.init()

    screen = pg.display.set_mode((width, height))   #依設定顯示視窗
    pg.display.set_caption("Game")           #設定程式標題

    clock = pg.time.Clock()
    font = pg.font.SysFont("Arial", 20)


    # Just a loading screen.
    screen.fill((0, 0, 0))
    screen.blit(font.render("Now Loading...", True, (255, 255, 255)), (width/2-100, height/2))

    pg.display.update()

    if cap is None:
        cap = cv2.VideoCapture(webcam_input_num)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
    detection = ObjectDetection(cap=cap)
    shuttlecocks = [] # 我需要有序的 所以不使用sprite group pg.sprite.Group()

    
    scoreBoard = ScoreBoard(0)
    TOTAL_CAN_PLAY_TIME = 30
    timer = Timer(TOTAL_CAN_PLAY_TIME)
    game_start_time = time.perf_counter()
    game_persists = 0


    running = True
    # while running:
    #     clock.tick(60)
    # 在這邊加一個準備完成的按鈕開始遊戲 避免 timer問題
        

    while running:
        screen.fill((255, 255, 255))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                
        
        now_time = time.perf_counter()
        game_persists = now_time - game_start_time
        timer.set_remain_time(TOTAL_CAN_PLAY_TIME - game_persists)
        if game_persists > 30:
            print(game_persists, game_start_time, now_time)
            running = False


        clock.tick()

        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            running = False
            continue
        
        frame = cv2.flip(frame, 1)
        results = detection(frame)
        filtered_results = filter_detections(results)
        collision_boxes = get_collision_detections(filtered_results)

        frame2 = np.rot90(frame)
        frame2 = cv2.flip(frame2, 0)
        frame2= cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        pg.surfarray.blit_array(screen, frame2)
        
        for row in collision_boxes:
            pg.draw.rect(screen, Color.GREEN, pg.Rect(row[0], row[1], row[2], row[3]), 2)

        if len(shuttlecocks) < 1 or now_time - shuttlecocks[-1].init_time > 1:
            new_shuttlecock = initail_new_shuttlecock(None, None)
            shuttlecocks.append(new_shuttlecock)

        for shuttlecock in shuttlecocks:
            shuttlecock.update()
            if shuttlecock.rect.bottom > height:
                shuttlecocks.remove(shuttlecock)
                # print("Removed")
            if shuttlecock.can_hit and len(filtered_results) > 0:
                for row in collision_boxes:
                    if pg.Rect(row[0], row[1], row[2], row[3]).colliderect(shuttlecock.rect):
                        shuttlecocks.remove(shuttlecock)
                        # print("HIT")
                        scoreBoard.score += 1
                        break

        scoreBoard.update()
        timer.update()

        for shuttlecock in shuttlecocks:
            shuttlecock.draw(screen)
        scoreBoard.draw(screen)
        timer.draw(screen)

        #screen.blit(font.render(f'builtin FPS:{clock.get_fps():.2f}', True, (0,255,0)), (100,70))
        pg.display.update()

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        

        screen.blit(font.render(f'SCORE: {scoreBoard.score}', True, (0,255,0)), (200,70))

        pg.display.update()
        clock.tick(60)

    pg.quit()           


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--Input', type=str, default='0', help='input webcam number')

    args = parser.parse_args()
    webcam_input_num = int(args.Input)

    stage2()