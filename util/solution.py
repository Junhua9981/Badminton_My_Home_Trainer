import mediapipe as mp
from util.math_util import *

class Solution:
    POSE = mp.solutions.pose.Pose(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    def __init__(self):
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_drawing = mp.solutions.drawing_utils

    def get_landmarks(self, w, h, results):
        pass

    def draw_landmarks(self, image, results):
        self.mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp.solutions.pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )

    @property
    def processor(self):
        return Solution.POSE

    @property
    def mode(self):
        return self._mode

    @staticmethod
    def landmarks_to_gradients(landmarks):
        lndmarks_record_array = []
        result_landmarks = landmarks
        for pos1, pos2 in mp.solutions.pose.POSE_CONNECTIONS:
            lndmarks_record_array.append(slopee(result_landmarks[pos1], result_landmarks[pos2]))
        #1
        lndmarks_record_array.append( calculate_angle( (result_landmarks[22].x, result_landmarks[22].y),(result_landmarks[16].x, result_landmarks[16].y), (result_landmarks[14].x, result_landmarks[14].y)) )
        #2
        lndmarks_record_array.append( calculate_angle( (result_landmarks[21].x, result_landmarks[21].y),(result_landmarks[15].x, result_landmarks[15].y), (result_landmarks[13].x, result_landmarks[13].y)) )
        #3
        lndmarks_record_array.append( calculate_angle( (result_landmarks[16].x, result_landmarks[16].y),(result_landmarks[14].x, result_landmarks[14].y), (result_landmarks[12].x, result_landmarks[12].y)) )
        #4
        lndmarks_record_array.append( calculate_angle( (result_landmarks[15].x, result_landmarks[15].y),(result_landmarks[13].x, result_landmarks[13].y), (result_landmarks[11].x, result_landmarks[11].y)) )
        #5
        lndmarks_record_array.append( calculate_angle( (result_landmarks[14].x, result_landmarks[14].y),(result_landmarks[12].x, result_landmarks[12].y), (result_landmarks[24].x, result_landmarks[24].y)) )
        #6
        lndmarks_record_array.append( calculate_angle( (result_landmarks[13].x, result_landmarks[13].y),(result_landmarks[11].x, result_landmarks[11].y), (result_landmarks[23].x, result_landmarks[23].y)) )
        #7
        lndmarks_record_array.append( calculate_angle( (result_landmarks[12].x, result_landmarks[12].y),(result_landmarks[24].x, result_landmarks[24].y), (result_landmarks[26].x, result_landmarks[26].y)) )
        #8
        lndmarks_record_array.append( calculate_angle( (result_landmarks[11].x, result_landmarks[11].y),(result_landmarks[23].x, result_landmarks[23].y), (result_landmarks[25].x, result_landmarks[25].y)) )
        #9
        lndmarks_record_array.append( calculate_angle( (result_landmarks[24].x, result_landmarks[24].y),(result_landmarks[26].x, result_landmarks[26].y), (result_landmarks[28].x, result_landmarks[28].y)) )
        #10
        lndmarks_record_array.append( calculate_angle( (result_landmarks[23].x, result_landmarks[23].y),(result_landmarks[25].x, result_landmarks[25].y), (result_landmarks[27].x, result_landmarks[27].y)) )
        
        return lndmarks_record_array
