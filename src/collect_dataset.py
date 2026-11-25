import cv2
import sys
import os


classes = ["snake", "ram", "monkey", "boar", "horse", "tiger", "other"]

while True:
    choice = input("Choose the class (snake, ram, monkey, boar, horse, tiger, other):").lower().strip()
    if choice not in classes:
        print("Please choose the correct class")
    else:
        break

data_path = os.path.join("data")
save_path = os.path.join(data_path, choice)
print(save_path)

cap = cv2.VideoCapture(0)
print(cap.isOpened())

if not cap.isOpened():
    sys.exit()

image_count = 0

while True:
    ret, frame = cap.read()
    
    if ret == False:
        break

    raw_frame = frame.copy()

    cv2.putText(frame, "Dataset Collection", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    cv2.putText(frame, f"Class : {choice}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imshow("Dataset Collection", frame)

    key = cv2.waitKey(1)
    
    if key == ord("s"):
        filename = f"{choice}_{image_count}.jpg"
        image_path = os.path.join(save_path, filename)
        success = cv2.imwrite(image_path, raw_frame)

        if success:
            print("Image captured")
            image_count += 1
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


