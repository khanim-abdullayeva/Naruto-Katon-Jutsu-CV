import cv2

cap = cv2.VideoCapture(0)
print(cap.isOpened())

while True:
    ret, frame = cap.read()
    
    if ret == False:
        break

    cv2.putText(frame, "Dataset Collection", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    cv2.imshow("Dataset Collection", frame)
    
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
