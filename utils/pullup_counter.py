import cv2
import mediapipe as mp
import numpy as np
import os, sys
from utils.db_management import log

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calc_angle(shoulder, elbow, wrist):
    a = np.array(shoulder)
    b = np.array(elbow)
    c = np.array(wrist)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle>180.0:
        angle = 360-angle

    return angle

async def count_reps(video):
    log.info("in the process of opening the video")
    cap = cv2.VideoCapture(f"./telegram/{video}")
    rips = 0
    direction = None
    
    log.info("Opened the video from the path")
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f"processed_videos/processed_{video}.avi", fourcc, 30, (frame_width, frame_height))  
    log.info("created VideoWriter instance")
    
    uped=False
    anti_cheater=0
    log.info("Calling MediaPipe Pose Detection model")
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        not_hanging=0
        hanging=0
        log.info("Passed into pose detection process successfully")
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

                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility
                left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility
                left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].visibility
                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility
                left_visibility = (left_shoulder + left_elbow + left_wrist + left_hip)/4

                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility
                right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility
                right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].visibility
                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility
                right_visibility = (right_shoulder + right_elbow + right_wrist + right_hip)/4
                
                if left_visibility > right_visibility:
                    cv2.putText(image, f"Left", [20, 160],
                                                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    mouth = [landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x, landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].y] 
                else:
                    cv2.putText(image, f"Right", [20, 160],
                                                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
                    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    mouth = [landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].x, landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].y] 
                
                arm_angle = calc_angle(shoulder, elbow, wrist)
                body_angle = calc_angle(hip, shoulder, elbow)

                #cv2.putText(image, f"shoulder: {str(shoulder[1])}", [20, 40],
                #                                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
                #cv2.putText(image, f"wrist: {str(wrist[1])}", [20, 60],
                #                                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
                #cv2.putText(image, f"arm_angle: {str(arm_angle)}", [20, 85],
                #                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                #cv2.putText(image, f"body_angle: {str(body_angle)}", [20, 110],
                #                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                #cv2.putText(image, f"reps: {str(rips)}", [20, 135],
                #                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                #cv2.putText(image, f"hanging: {hanging}", [20, 185],
                #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
                #mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                out.write(image)
                

                if shoulder[1]-wrist[1]>=0:
                    hanging+=1
                elif shoulder[1]-wrist[1]<-0.04:
                    hanging=0
                    uped=False
                    continue

                if hanging>=20:
                    not_hanging=0
                    if arm_angle<110 and body_angle<100:
                        if (shoulder[1]>=wrist[1] and shoulder[1]-wrist[1]<=0.05) or wrist[1]-shoulder[1]<=0.077:
                            anti_cheater=wrist[1]
                            uped=True
                    elif arm_angle>90 and body_angle>90:
                            if uped and np.abs(anti_cheater-wrist[1])<0.05:
                                rips+=1
                                uped=False

                    if not_hanging>=15:
                        not_hanging=0


            except Exception as e:
                log.error(e)

            #if cv2.waitKey(10) & 0xFF == ord('q'):
            #    break

        out.release()
        cap.release()
        cv2.destroyAllWindows()
    return rips    


