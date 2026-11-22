import mediapipe as mp
import cv2
import time

cap = cv2.VideoCapture(0)
print(cap.isOpened())
prev_time = time.perf_counter()

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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

