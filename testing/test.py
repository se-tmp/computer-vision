from ultralytics import YOLO
import cv2
import math 
# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

model = YOLO("pretrained_model.pt")
classNames = ["Lying", "Sitting", "Standing", ""]

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    for r in results:
        boxes = r.boxes

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            if(cls==0):
                color = (0, 255, 255)
            elif(cls==1):
                color = (255, 0, 255)
            else:
                color = (255, 255, 0)

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 5)

            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 4
            thickness = 10

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()