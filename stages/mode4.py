from typing import Tuple
from unittest import result
from cv2 import blur
import pygame as pg
import argparse
import cv2
import numpy as np
import time
import csv
import mediapipe as mp
import enum
from addDB import addDB
from util.color import Color
from util.frame import *
from util.solution import Solution
from charactor.final_score import FinalGradeBoard, BackButton
from charactor.scoreboard import SimilarityBoard


width, height = 1920, 1080                  #遊戲畫面寬和高
height -= 70                                #視窗工作列高度

class Target_Landmark:
    def __init__(self, video_path, target_csv) -> None:
        
        print("video_path:", video_path)
        self.video = cv2.VideoCapture(video_path)
        self.is_video_pause = False     
        with open(target_csv, mode='r', newline='') as  f:
            self.target_landmarks = list( csv.reader(f) )
        # header format : #, video_path , vid_width , vid_height , total_frame_number , pose_record lines
        if self.target_landmarks[0][0] == '#':
            self.vid_width = int(self.target_landmarks[0][2])
            self.vid_height = int(self.target_landmarks[0][3])
            self.frame_per_record = int(self.target_landmarks[0][6])
            self.pose_record_lines = int(self.target_landmarks[0][5])
            self.total_frame_number = int(self.target_landmarks[0][4])
            print("vid_width:", self.vid_width)
            print("vid_height:", self.vid_height)
            print("frame_per_record:", self.frame_per_record)
            print("total_frame_number:", self.total_frame_number)
            self.target_landmarks = self.target_landmarks[1:] # 拋棄header
        else:
            self.target_landmarks = self.target_landmarks
        self.current_frame_num = 0
        self.current_record= self.current_frame_num//self.frame_per_record
        self.pre_video_frame = None
        self.now_video_frame = None

    # 回傳影片的當前frame, 及當前frame的landmark的位置
    def frame(self) -> Tuple[np.ndarray, int, int]:
        if self.is_video_pause:
            # self.video.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_num)
            # ret, frame = self.video.read()
            # frame = self.pre_video_frame
            # if not ret:
                # return None, self.current_frame_num, self.current_record
            return self.now_video_frame, self.current_frame_num, self.current_record
        else:
            ret, self.now_video_frame = self.video.read()
            if ret:
                self.current_frame_num = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
                self.current_record = self.current_frame_num//self.frame_per_record
                return self.now_video_frame, self.current_frame_num, self.current_record
            else:
                return None, -1, -1
        # else:
        #     return None, -1, -1
    
    def seek(self, frame_num) -> None:
        self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        self.current_frame_num = frame_num
        self.current_record = frame_num//self.frame_per_record

    # 獲取當前landmark
    def get_clandmark(self) -> np.ndarray:
        return self.get_landmark(self.current_frame_num)

    # 獲取前一個landmark
    def get_plandmark(self) -> np.ndarray:
        return self.get_landmark(max(self.current_frame_num-1, 0))

    # 獲取 frame_num 的 frame的landmark
    def get_landmark(self, frame_num) -> np.ndarray:
        if "X" in self.target_landmarks[frame_num//self.frame_per_record]:
            return None
        else:
            return np.array(self.target_landmarks[frame_num//self.frame_per_record], dtype=np.float32)

    @property
    def is_end(self) -> bool:
        return self.current_frame_num >= self.total_frame_number


class PoseAngle(enum.IntEnum):
# 抱歉和mediapipe的定義不同，右手為單數，左手為雙數
# mediapipe的定義：左手為單數，右手為雙數
    RIGHT_WRIST    = 35 # 66
    LEFT_WRIST     = 36 # 67
    RIGHT_ELBOW    = 37 # 68
    LEFT_ELBOW     = 38 # 69
    RIGHT_SHOULDER = 39 # 70
    LEFT_SHOULDER  = 40 # 71
    RIGHT_HIP      = 41 # 72
    LEFT_HIP       = 42 # 73
    RIGHT_KNEE     = 43 # 74
    LEFT_KNEE      = 44 # 75

class PoseGradient(enum.IntEnum):
    """Only implement what i need"""
    LEFT_SHOULDER = 10
    LEFT_ELBOW = 11
    RIGHT_SHOULDER = 16
    RIGHT_ELBOW = 17
    LEFT_THIGH = 25
    RIGHT_THIGH = 26
    LEFT_CALF = 27
    RIGHT_CALF = 28

POSE_GRADIENT = [10 , 11 , 16 , 17 , 25 , 26 , 27 , 28]
ANGLES_TAB = frozenset([(35,16), (36,15), (37,14), (38,13), (39,12), (40,11), (41,24), (42,23), (43,26), (44,25)])
# ANGLES_TAB = frozenset([(35,16), (36,15), (37,14), (38,13), (39,12), (40,11)])
# ANGLES_TAB = frozenset([(37,14), (38,13), (39,12), (40,11)])


wrong_angles = []

# python .\stages\mode4.py cap
def stage4(cap, target_video, target_csv):
    global width, height
    # 初始化pygame
    pg.init()

    screen = pg.display.set_mode((width,height), pg.RESIZABLE)   #依設定顯示視窗
    pg.display.set_caption("Game")           #設定程式標題

    clock = pg.time.Clock()
    font = pg.font.Font("assets/fonts/monogram/ttf/monogram.ttf", 24)
    score_font = pg.font.Font("assets/fonts/monogram/ttf/monogram.ttf", 54)

    if pg.mixer.get_init() is None:
        pg.mixer.init()

    pg.mixer.music.load("assets/music/BGM.mp3")
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play(-1)

    solution = Solution()

    # Just a loading screen.
    screen.fill((0, 0, 0))
    screen.blit(font.render("Now Loading...", True, (255, 255, 255)), (width/2-100, height/2))

    pg.display.update()

    # cap = cv2.VideoCapture(r".\video\smash\step_1_racket_posing.wmv")
    if cap is None:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    target_landmark = Target_Landmark(target_video, target_csv)

    wrong_angles = []
    diff_angs = []
    running = True
    score = 0
    sum_score = 0
    game_start_time = time.perf_counter()
    similarityBoard = SimilarityBoard()


    while running:
        screen.fill((255, 255, 255))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                return
                
        now_time = time.perf_counter()
        game_persists = now_time - game_start_time

        if target_landmark.is_end:
            running = False
            break

        clock.tick()

        ret, frame = cap.read()
        
        if not ret:
            print("Failed to capture image")
            running = False
            continue
        frame = cv2.resize(frame, (width, height))
        # mspos = pg.mouse.get_pos()
        # if mspos[0] > width/2 or mspos[1] > height/2:
        #     target_landmark.is_video_pause = True
        # else:
        #     target_landmark.is_video_pause = False
        # target_landmark.is_video_pause = True

        target_frame, current_frame_num, current_record = target_landmark.frame()

        frame = cv2.flip(frame, 1)
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = solution.processor.process(frame)
        solution.draw_landmarks(frame, result)
        if result.pose_landmarks is not None:
            landmark_result = result.pose_landmarks.landmark
            gradient_result = Solution.landmarks_to_gradients(landmark_result)
        else:
            target_landmark.seek(current_frame_num)
            continue

        # frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)


        
        if target_frame is None:
            print("Failed to capture video")
            running = False
            continue
        else:
            # cv2.putText(target_frame, "{}".format(current_frame_num), (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 6)
            target_width, target_height = int(width//2), int(height//2)
            target_surf = cv_frame_to_pygame_surface(target_frame, target_width, target_height)


            

        # if len(TIME_TO_DETECT)>0 and current_frame_num + 5 > TIME_TO_DETECT[0][1]:

        if current_frame_num % target_landmark.frame_per_record == 0:
            # for idx in POSE_GRADIENT:
            #     player_gradient = gradient_result[idx]
            #     target_gradient = target_landmark.get_clandmark()[idx]
            #     print( player_gradient, target_gradient,sep='\t' ,end="\t")
            #     diff_ang =int(np.fabs(np.arctan((player_gradient-target_gradient)/(float(1 + player_gradient*target_gradient)))*180/np.pi)+0.5)
            #     print(diff_ang)
            diff_angs = []
            wrong_angles = []
            score = 0
            for angle in ANGLES_TAB:
                player_angle = gradient_result[angle[0]]
                if target_landmark.get_clandmark() is None:
                    break
                target_angle = target_landmark.get_clandmark()[angle[0]]

                if target_angle > player_angle:
                    diff_ang = target_angle - player_angle
                    if diff_ang > 180:
                        diff_ang = 360 - diff_ang
                else:
                    diff_ang = player_angle - target_angle
                    if diff_ang > 180:
                        diff_ang = 360 - diff_ang
                # print(player_angle, target_angle, diff_ang, sep='\t', end="\n")
                if( diff_ang > 30 ):
                    wrong_angles.append([landmark_result[angle[1]].x *width, landmark_result[angle[1]].y*height, player_angle, target_angle, diff_ang])
                else:
                    score += np.sin( diff_ang /30*1.4 + np.pi/2) * 100/len(ANGLES_TAB)
                diff_angs.append(abs(diff_ang))
            # sum_of_diff = sum(diff_angs)
            # player_angle = gradient_result[35]
            # target_angle = target_landmark.get_clandmark()[35]
            # sum_of_diff = target_angle - player_angle
            # print(diff_angs, sep='\t', end="\n")
            # print(f"{player_angle}\t{target_angle}")
            # print(f"========={sum_of_diff}===={len(wrong_angles)}===")

        

        # if len(wrong_angles) > 0:
        #     target_landmark.is_video_pause = True
        #     # target_landmark.seek(current_frame_num-1)
        # else:
        #     target_landmark.is_video_pause = False


        # for idx , i in ANGLES_TAB:
            # cv2.putText(frame, str(diff_angs[idx]), ( gradient_result[i[1]].x, gradient_result[i[1]].y ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        pg.surfarray.blit_array(screen, np_frame_to_pygame_ori(frame)) # 玩家畫面


        for w in wrong_angles:
            pg.draw.circle(screen, Color.RED, (w[0], w[1]), 50, 5)
            # screen.blit(font.render(f"{w[3]:.2f} {w[4]:.2f}", True, Color.RED), (w[0], w[1]))
        screen.blit(font.render(f"{score:.2f}", True, Color.RED), (10, 10))  # 當前相似度
        similarityBoard.score=f"{score:.2f}%"
        similarityBoard.update()
        similarityBoard.draw(screen)
        sum_score+=score

        screen.blit(target_surf, (width/2, 0)) # 影片畫面放在右上角

        # if len(TIME_TO_DETECT)>0 and current_frame_num + 5 > TIME_TO_DETECT[0][1]:
        #     pg.draw.rect(screen, Color.RED, (0, 0, width, height), 5)
        # elif len(TIME_TO_DETECT)>0 and current_frame_num < TIME_TO_DETECT[0][1]:
        #     TIME_TO_DETECT.pop(0)


        #screen.blit(font.render(f'builtin FPS:{clock.get_fps():.2f}', True, Color.GREEN), (100,70))
        pg.display.update()

    running = True
    #TODO: put the game over screen
    final_scoreboard = FinalGradeBoard(f"{sum_score/target_landmark.pose_record_lines:.2f}%")
    back_button = BackButton()

    blur_size = 1
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                running = False if back_button.check_click(event.pos) else True
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
    time_string = time.strftime("%Y-%m-%d %H:%M:%S %p", localtime)
    now_type = target_video.split('\\')[-2]
    step_num = target_video.split('\\')[-1][:6]
    addDB(str(time_string), "訓練模式"+now_type+step_num, str(sum_score//target_landmark.pose_record_lines))
    pg.quit()
    # cap.release()
    return None


if __name__ == '__main__':
    # python .\stages\mode4.py -i 0 

    import os
    parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    video_path = parent_path + r'\Video\backcourt_architecture\correct_full_step.wmv'
    csv_path = parent_path + r'\mode4_data\backcourt_architecture\correct_full_step.csv'
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--Input', type=str, default='0', help='input webcam number')
    parser.add_argument('-v', '--video_path', type=str, default= video_path, help='input webcam number')
    parser.add_argument('-c', '--csv_path', type=str, default= csv_path, help='input webcam number')

    args = parser.parse_args()
    webcam_input_num = int(args.Input)
    video_path = args.video_path
    csv_path = args.csv_path

    cap = cv2.VideoCapture(0)
    stage4(cap, video_path, csv_path)