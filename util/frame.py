import cv2 
import numpy as np
import pygame as pg

def cv_frame_to_pygame_frame_mirror(frame, width, height):
    frame = cv2.resize(frame, (width, height))
    frame2 = np.rot90(frame)
    frame2 = cv2.flip(frame2, 0)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    return frame2

def cv_frame_to_pygame_surface(frame, width, height):
    target_frame = cv_frame_to_pygame_frame_mirror(frame, width, height)
    target_surface = pg.surface.Surface((width, height))
    pg.surfarray.blit_array(target_surface, target_frame)
    target_frame = pg.transform.scale(target_surface, (width, height))
    return target_frame

def np_frame_to_pygame_ori(frame):
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = cv2.flip(frame, 0)
    return frame