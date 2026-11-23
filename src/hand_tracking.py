import mediapipe as mp
import cv2
import numpy as np
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarksConnections

model_path = "models/hand_landmarker.task"
base_options = python.BaseOptions(model_asset_path = model_path)
options = vision.HandLandmarkerOptions(
    base_options = base_options,
    running_mode = vision.RunningMode.VIDEO,
    num_hands = 2
)
landmarker = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
print(cap.isOpened())
prev_time = time.perf_counter()
start_time = time.perf_counter()

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    
    height, width = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = rgb_frame)
    timestamp_ms = int((time.perf_counter() - start_time) * 1000)
    result = landmarker.detect_for_video(mp_image, timestamp_ms)
    connections = HandLandmarksConnections.HAND_CONNECTIONS
    
    for hand in result.hand_landmarks:
        for landmark in hand:
            px = int(landmark.x * width)
            py = int(landmark.y * height)
            cv2.circle(frame, (px,py), 4, (0, 255, 0), -1)
            
            fingers = {
                "Index" : (8, 6),
                "Middle": (12, 10),
                "Ring" : (16,14),
                "Pinky" : (20, 18)
                }
            
            for i, finger in enumerate(fingers):
                tip_idx, pip_idx = fingers[finger]

                tip_y = hand[tip_idx].y
                pip_y = hand[pip_idx].y

                if tip_y < pip_y:
                    status = "Extended"
                else:
                    status = "Bent"

                y_position = 120 + i * 30

                cv2.putText(
                    frame, f"{finger}: {status}", (50, y_position), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 180, 0),2
                    )
        
        mcp = hand[5]
        pip = hand[6]
        tip = hand[8]


        v1 = (mcp.x - pip.x, mcp.y - pip.y)
        v2 = (tip.x - pip.x, tip.y - pip.y)

        dot_product = np.dot(v1, v2)

        length_v1 = np.linalg.norm(v1)
        length_v2 = np.linalg.norm(v2)

        denominator = length_v1 * length_v2

        if denominator > 0:
            cos_theta = dot_product / denominator
            cos_theta = np.clip(cos_theta, -1, 1)
            angle = np.degrees(np.arccos(cos_theta))
        else:
            angle = None

        if angle >= 160:
            status = "Extended"
        else:
            status = "Bent"
        
        cv2.putText(frame, f"Index: {status} | Angle: {angle}", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),2)
        

            
        for connection in connections:
            start_idx = connection.start
            end_idx = connection.end
        
            start_landmark = hand[start_idx]
            end_landmark = hand[end_idx]
        
            start_x = int(start_landmark.x * width)
            start_y = int(start_landmark.y * height)
        
            end_x = int(end_landmark.x * width)
            end_y = int(end_landmark.y * height)
        
            cv2.line(frame, (start_x,start_y), (end_x, end_y), (255, 255, 255), 2)


    cv2.putText(frame,"Katon Gokakyu No Jutsu", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
    current_time = time.perf_counter()
    delta_time = current_time - prev_time
    if delta_time > 0:
        fps = 1 / delta_time
    else:
        fps = 0

    cv2.putText(frame, f"FPS : {fps:.1f}", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (224, 255, 255), 1)
    cv2.imshow("Katon Jutsu", frame)
    prev_time = current_time
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()



