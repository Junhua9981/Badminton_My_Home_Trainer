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
from charactor.final_score import FinalScoreBoard, BackButton
from addDB import addDB
from util.color import Color
from util.evaluation_string import Evaluation_strings
from util.sound_effects import swing_sound_effects
from util.frame import np_frame_to_pygame_ori

width, height = 1920, 1080                  #遊戲畫面寬和高
height -= 70                                #視窗工作列高度
hit_size = 0.7 #接觸方框縮放

#################################
##        這是左右拋的小球        ##
#################################

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


BALL_POSITION_ARR = [
    {'start_pos': (0, height/3), 'throw_dir': 1},
    {'start_pos': (width, height/3), 'throw_dir': -1},
]


def initail_new_shuttlecock(start_pos: Tuple[int, int], speed: Tuple[int, int]):
    basic_set = random.choice(BALL_POSITION_ARR)

    if start_pos is Tuple:
        new_shuttlecock = Shuttlecock(start_pos)
    elif start_pos is None:
        new_shuttlecock = Shuttlecock(basic_set['start_pos'])
    if speed is Tuple:
        new_shuttlecock.set_speed( speed )
    elif speed is None:
        new_shuttlecock.set_speed(
            pg.math.Vector2( basic_set['throw_dir'] * random.randint(3, 5), random.randint(-10, -5) )
            )
    return new_shuttlecock

def stage2_2(cap, detection):
    global width, height

    # 初始化pygame
    pg.init()

    screen = pg.display.set_mode((width, height))   #依設定顯示視窗
    pg.display.set_caption("Game")           #設定程式標題

    clock = pg.time.Clock()
    
    font = pg.font.Font("assets/fonts/monogram/ttf/monogram.ttf", 24)
    score_font = pg.font.Font("assets/fonts/monogram/ttf/monogram.ttf", 54)

    if pg.mixer.get_init() is None:
        pg.mixer.init()

    pg.mixer.music.load("assets/music/BGM.mp3")
    pg.mixer.music.set_volume(0.6)
    pg.mixer.music.play(-1)

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
    scores_on_screen = []
    racket_pos_record = [pg.Vector2(0,0), pg.Vector2(0,0)]
    speed_of_racket = 0.0
    should_play_swing_sound = False

    
    scoreBoard = ScoreBoard(0)
    TOTAL_CAN_PLAY_TIME = 20
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
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
        
        now_time = time.perf_counter()
        game_persists = now_time - game_start_time
        timer.set_remain_time(TOTAL_CAN_PLAY_TIME - game_persists + 1)
        if game_persists > TOTAL_CAN_PLAY_TIME:
            # print(game_persists, game_start_time, now_time)
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
        frame2 = cv2.resize(frame2, (height,width), interpolation = cv2.INTER_AREA)
        pg.surfarray.blit_array(screen, frame2)
        
        # for row in collision_boxes:
        #     pg.draw.rect(screen, Color.GREEN, pg.Rect(row[0], row[1], row[2], row[3]), 2)
        if len(collision_boxes) == 1:
            racket_pos_record.append( pg.Vector2(collision_boxes[0][0]+collision_boxes[0][2]/2, collision_boxes[0][1]+collision_boxes[0][3]/2) )
            racket_pos_record.pop(0)
            speed_of_racket = racket_pos_record[0].distance_to(racket_pos_record[1])
            if speed_of_racket > 75.0:
                should_play_swing_sound = True
        
        if should_play_swing_sound:
            swing_sound_effects.play()
            should_play_swing_sound = False

                #       如果沒球在畫面上 或是 最後一顆球出現1.5秒以上了 就再產生一顆球
        if len(shuttlecocks) < 1 or now_time - shuttlecocks[-1].init_time > 1.5:
            new_shuttlecock = initail_new_shuttlecock(None, None)
            shuttlecocks.append(new_shuttlecock)

        for shuttlecock in shuttlecocks:
            shuttlecock.update()
            if shuttlecock.rect.bottom > height * 1.2 or (not shuttlecock.far_to_close and shuttlecock.size < 30):
                shuttlecocks.remove(shuttlecock)
                # print("Removed")
            
            if shuttlecock.can_hit and len(filtered_results) > 0:
                for row in collision_boxes:
                    if pg.Rect(row[0], row[1], row[2], row[3]).colliderect(shuttlecock.rect):
                        scoreBoard.score += shuttlecock.score
                        scores_on_screen.append( [ random.choice(Evaluation_strings), row[0] + random.randint(0, int(row[2])), row[1] + random.randint(0, int(row[3])) , 0 , 255] )
                        # 放的是 [ 分數, 顯示位置的x, y , 時間, 透明度 ]
                        if shuttlecock.far_to_close:
                            shuttlecock.set_far_to_close(False)
                        # shuttlecocks.remove(shuttlecock)
                        # print("HIT")
                        break

        
        for score in scores_on_screen:
            text_surf = score_font.render("+"+str(score[0]), True, Color.BLACK)
            text_surf.set_alpha(score[4])
            screen.blit(text_surf,  (score[1], score[2]))
            score[4] -= 255/20 # 透明度減少10%
            score[3] += 1 # 時間+1
            if score[3] > 20: # 顯示10/25秒之後消失
                scores_on_screen.remove(score)


        scoreBoard.update()
        timer.update()

        for shuttlecock in shuttlecocks:
            shuttlecock.draw(screen)
        scoreBoard.draw(screen)
        timer.draw(screen)

        #screen.blit(font.render(f'builtin FPS:{clock.get_fps():.2f}', True, (0,255,0)), (100,70))
        pg.display.update()

    running = True
    final_scoreboard = FinalScoreBoard(scoreBoard.score)
    back_button = BackButton()
    blur_size = 1

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                running = False if back_button.check_click(event.pos) else running

        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.GaussianBlur(frame, (blur_size, blur_size), 0)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (width, height))
            pg.surfarray.blit_array(screen, np_frame_to_pygame_ori(frame))
            blur_size += 2 if blur_size < 71 else 0

        final_scoreboard.update()
        final_scoreboard.draw(screen)
        back_button.draw(screen)
        pg.display.update()
        clock.tick(60)
    localtime = time.localtime()
    result = time.strftime("%Y-%m-%d %H:%M:%S %p", localtime)
    str(result)
    addDB( result, "專項訓練-左右小球練習", scoreBoard.score)
    pg.quit()        
    # cap.release()
    return detection   


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--Input', type=str, default='0', help='input webcam number')

    args = parser.parse_args()
    webcam_input_num = int(args.Input)

    stage2_2()