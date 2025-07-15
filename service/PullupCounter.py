import cv2
import mediapipe as mp
import numpy as np
from .utils import LOG 

MP_DRAWING = mp.solutions.drawing_utils
MP_POSE = mp.solutions.pose
class PullupCounter:

    @staticmethod
    def _calc_angle(shoulder, elbow, wrist):
        a = np.array(shoulder)
        b = np.array(elbow)
        c = np.array(wrist)
    
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
    
        if angle>180.0:
            angle = 360-angle
    
        return angle

    @staticmethod
    def _get_visible_side(landmarks, image):
        left_shoulder = landmarks[MP_POSE.PoseLandmark.LEFT_SHOULDER.value].visibility
        left_elbow = landmarks[MP_POSE.PoseLandmark.LEFT_ELBOW.value].visibility
        left_wrist = landmarks[MP_POSE.PoseLandmark.LEFT_WRIST.value].visibility
        left_hip = landmarks[MP_POSE.PoseLandmark.LEFT_HIP.value].visibility
        left_visibility = (left_shoulder + left_elbow + left_wrist + left_hip)/4
    
        right_shoulder = landmarks[MP_POSE.PoseLandmark.RIGHT_SHOULDER.value].visibility
        right_elbow = landmarks[MP_POSE.PoseLandmark.RIGHT_ELBOW.value].visibility
        right_wrist = landmarks[MP_POSE.PoseLandmark.RIGHT_WRIST.value].visibility
        right_hip = landmarks[MP_POSE.PoseLandmark.RIGHT_HIP.value].visibility
        right_visibility = (right_shoulder + right_elbow + right_wrist + right_hip)/4
        
        if left_visibility > right_visibility:
            cv2.putText(image, f"Left", [20, 160],
                                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
            shoulder = [landmarks[MP_POSE.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[MP_POSE.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[MP_POSE.PoseLandmark.LEFT_ELBOW.value].x, landmarks[MP_POSE.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[MP_POSE.PoseLandmark.LEFT_WRIST.value].x, landmarks[MP_POSE.PoseLandmark.LEFT_WRIST.value].y]
            hip = [landmarks[MP_POSE.PoseLandmark.LEFT_HIP.value].x, landmarks[MP_POSE.PoseLandmark.LEFT_HIP.value].y]
            mouth = [landmarks[MP_POSE.PoseLandmark.MOUTH_LEFT.value].x, landmarks[MP_POSE.PoseLandmark.MOUTH_LEFT.value].y] 
        else:
            cv2.putText(image, f"Right", [20, 160],
                                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
            shoulder = [landmarks[MP_POSE.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[MP_POSE.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[MP_POSE.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[MP_POSE.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist = [landmarks[MP_POSE.PoseLandmark.RIGHT_WRIST.value].x, landmarks[MP_POSE.PoseLandmark.RIGHT_WRIST.value].y]
            hip = [landmarks[MP_POSE.PoseLandmark.RIGHT_HIP.value].x, landmarks[MP_POSE.PoseLandmark.RIGHT_HIP.value].y]
            mouth = [landmarks[MP_POSE.PoseLandmark.MOUTH_RIGHT.value].x, landmarks[MP_POSE.PoseLandmark.MOUTH_RIGHT.value].y] 
        return shoulder, elbow, wrist, hip, mouth

    @staticmethod
    def _depict_lines(image, shoulder, elbow, wrist, hip, mouth, arm_angle, body_angle, hanging, reps, result):
        cv2.putText(image, f"shoulder: {str(shoulder[1])}", [20, 40],
                                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, f"wrist: {str(wrist[1])}", [20, 60],
                                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, f"arm_angle: {str(arm_angle)}", [20, 85],
                                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, f"body_angle: {str(body_angle)}", [20, 110],
                                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, f"reps: {str(reps)}", [20, 135],
                                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, f"hanging: {hanging}", [20, 185],
                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
        MP_DRAWING.draw_landmarks(image, result.pose_landmarks, MP_POSE.POSE_CONNECTIONS)



    @staticmethod
    def count_reps(video):
        LOG.info("in the process of opening the video")
        cap = cv2.VideoCapture(f"./telegram/videos/{video}")
        rips = 0

        LOG.info("Opened the video from the path")
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(f"processed_videos/processed_{video}.avi", fourcc, 30, (frame_width, frame_height))  
        LOG.info("created VideoWriter instance")

        uped=False
        anti_cheater=0
        LOG.info("Calling MediaPipe Pose Detection model")
        with MP_POSE.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            not_hanging=0
            hanging=0
            LOG.info("Passed into pose detection process successfully")
            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    break

                #Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                image.flags.writeable = False

                #Make Detection
                result = pose.process(image)

                #Recolor image to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                #Extract Landmarks
                try:
                    landmarks = result.pose_landmarks.landmark

                    shoulder, elbow, wrist, hip, mouth = PullupCounter._get_visible_side(landmarks, image)
 

                    arm_angle = PullupCounter._calc_angle(shoulder, elbow, wrist)
                    body_angle = PullupCounter._calc_angle(hip, shoulder, elbow)
                    PullupCounter._depict_lines(image, shoulder, elbow, wrist, hip, mouth, arm_angle, body_angle, hanging, rips, result)
                    out.write(image)

                    if shoulder[1]-wrist[1]>=0:
                        hanging+=1
                    elif shoulder[1]-wrist[1]<-0.04:
                        hanging=0
                        uped=False

                    if hanging>=20:
                        if arm_angle<110 and body_angle<100:
                            if (shoulder[1]>=wrist[1] and shoulder[1]-wrist[1]<=0.05) or wrist[1]-shoulder[1]<=0.077:
                                anti_cheater=wrist[1]
                                uped=True
                        elif arm_angle>90 and body_angle>90:
                                if uped and np.abs(anti_cheater-wrist[1])<0.05:
                                    rips+=1
                                    uped=False

                except Exception as e:
                    LOG.error(e)

            out.release()
            cap.release()
            cv2.destroyAllWindows()
        return rips    


