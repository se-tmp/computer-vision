import traceback
from ultralytics import YOLO
import cv2, math, time, signal, sys
from ThreadedCamera import ThreadedCamera
from Processor import Processor, classNames
import os

model_path = "./model.pt" if "IN_CONTAINER" in os.environ else "../model.pt"
model = YOLO(model_path)
rtmpAddress = os.environ.get("RTMPADDRESS")

def signal_handler(sig, frame):
    sys.exit(0)
    
def draw_for_test(img, x1, y1, x2, y2, cls):
    if(cls==0):
        color = (0, 255, 255)
    elif(cls==1):
        color = (255, 0, 255)
    else:
        color = (255, 255, 0)

    cv2.rectangle(img, (x1, y1), (x2, y2), color, 5)

    confidence = math.ceil((box.conf[0]*100))/100
    # print("Confidence --->",confidence)

    org = [x1, y1]
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 4
    thickness = 10

    cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
     
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    processor = Processor(1)
    while True:
        threaded_camera = ThreadedCamera(rtmpAddress)
        time.sleep(1)

        while True:
            try:
                if os.environ.get("IN_CONTAINER") == "":
                    threaded_camera.show_frame()
                img = threaded_camera.read()
                results = model(img, stream=True, verbose=False)
                w, h = 1280, 720

                for r in results:
                        boxes = r.boxes
                        for box in boxes:
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            cls = int(box.cls[0])
                            
                            targetPoint: tuple[tuple[float, float], tuple[float, float], str] = ((x1/w, y1/h), (x2/w, y2/h), classNames[cls])
                            processor.push(targetPoint)
                            # print((x1/w, y1/h), (x2/w, y2/h))
                            # print("Class name -->", classNames[cls])
                            draw_for_test(img, x1, y1, x2, y2, cls)
            except:
                print("connection failed..")
                traceback_message = traceback.format_exc()
                print(traceback_message)
                time.sleep(2)
                break


