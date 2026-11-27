import cv2
import sys
import os
import time

def save_image(choice, image_count, save_path, raw_frame):
    filename = f"{choice}_{image_count}.jpg"
    image_path = os.path.join(save_path, filename)
    success = cv2.imwrite(image_path, raw_frame)
    
    return success


classes = ["snake", "ram", "monkey", "boar", "horse", "tiger", "other"]

while True:
    choice = input("Choose the class (snake, ram, monkey, boar, horse, tiger, other):").lower().strip()
    if choice not in classes:
        print("Please choose the correct class")
    else:
        break

data_path = os.path.join("data")
save_path = os.path.join(data_path, choice)
os.makedirs(save_path, exist_ok = True)
existing_files = os.listdir(save_path)

image_numbers = []

for image in existing_files:
    if image.endswith(".jpg"):
        if "_" in image:
            file_extension = os.path.splitext(image)
            file_name_num = file_extension[0].split("_")
            if file_name_num[1].isdigit():
                file_num = int(file_name_num[1])
                image_numbers.append(file_num)
        


print(image_numbers)

if len(image_numbers) == 0:
    image_count = 0
else:
    image_count = max(image_numbers) + 1

target_count = 500
total_images = len(image_numbers)

cap = cv2.VideoCapture(0)
print(cap.isOpened())

if not cap.isOpened():
    sys.exit()

auto_capture = False
capture_interval = 1.0
last_capture_time = 0

while True:
    ret, frame = cap.read()
    
    if ret == False:
        break

    raw_frame = frame.copy()

    if auto_capture == False:
        status = "Off" 
    else:
        status = "On"

    cv2.putText(frame, "Dataset Collection", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(frame, f"Class : {choice}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"Target count: {target_count} | Total images: {total_images}", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 1)
    cv2.putText(frame, f"Auto capture: {status}", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow("Dataset Collection", frame)

    key = cv2.waitKey(1)
    
    if key == ord("s"):
        if total_images < target_count:
            success =  save_image(choice, image_count, save_path, raw_frame)
            if success:
                print("Image captured manually")
                image_count += 1
                total_images += 1
        else:
            print("Limit reached")
    elif key == ord("a"):
        if total_images < target_count:
            auto_capture = True
            last_capture_time = time.perf_counter()
        else:
            auto_capture = False
            print("Limit reached")
    elif key == ord("p"):
        auto_capture = False
    elif key == ord("q"):
        break

    if auto_capture == True and total_images < target_count:
        current_time = time.perf_counter()
        elapsed_time = current_time - last_capture_time
        if elapsed_time >= capture_interval:
            success = save_image(choice, image_count, save_path, raw_frame)
            last_capture_time = current_time

            if success:
                print("Image captured automatically")
                image_count += 1
                total_images += 1
    if total_images >= target_count:
        if auto_capture == True:
            print("Limit reached")
            auto_capture = False

print(image_count)
print(image_numbers)

cap.release()
cv2.destroyAllWindows()

