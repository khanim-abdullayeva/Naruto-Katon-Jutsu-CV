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
    hands_states = {}
    
    for hand_idx, hand in enumerate(result.hand_landmarks):
        hand_label = result.handedness[hand_idx][0].category_name
        
        if hand_label == "Left":
            x_position = 20
        else:
            x_position = width // 2 + 20

        cv2.putText(frame, f"{hand_label} hand", (x_position, 110), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2 )

        for landmark in hand:
            px = int(landmark.x * width)
            py = int(landmark.y * height)
            cv2.circle(frame, (px,py), 4, (0, 255, 0), -1)
            
        fingers = {
            "Thumb" : (1, 2, 4),
            "Index": (5, 6, 8),
            "Middle": (9, 10, 12),
            "Ring": (13, 14, 16),
            "Pinky": (17, 18, 20)
            }
        
        thumb_tip = hand[4]
        index_mcp = hand[5]
        wrist = hand[0]
        middle_mcp = hand[9]
        
        thumb_vector = (
        (thumb_tip.x - index_mcp.x) * width,
        (thumb_tip.y - index_mcp.y) * height
        )
        
        thumb_distance = np.linalg.norm(thumb_vector)
        
        palm_vector = (
        (middle_mcp.x - wrist.x) * width,
        (middle_mcp.y - wrist.y) * height
        )
        
        palm_size = np.linalg.norm(palm_vector)
        
        if palm_size > 0:
            thumb_ratio = thumb_distance / palm_size
        else:
            thumb_ratio = None

            
        finger_states = {}

        for i, (finger, indices) in enumerate(fingers.items()): 
            mcp_idx, pip_idx, tip_idx = indices
                
            mcp = hand[mcp_idx]
            pip = hand[pip_idx]
            tip = hand[tip_idx]


            v1 = ((mcp.x - pip.x) * width, (mcp.y - pip.y) * height)
            v2 = ((tip.x - pip.x) * width, (tip.y - pip.y) * height)

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

            if angle is None:
                status = "Unknown"

            elif finger == "Thumb":
                if thumb_ratio is None:
                    status = "Unknown"
                elif angle >= 160 and thumb_ratio >= 0.5:
                    status = "Extended"
                else:
                    status = "Bent"

            elif angle >= 160:
                status = "Extended"
            else:
                status = "Bent"
        
            finger_states[finger] = status
    

            if angle is not None:
                text = f"{finger}: {status} | {angle:.1f}"
            else:
                text = f"{finger}: {status}"

                
            y_position = 140 + i * 30

            cv2.putText(frame, text, (x_position, y_position), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),2)
            
        
        hands_states[hand_label] = finger_states   
        
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

    print(hands_states)
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



