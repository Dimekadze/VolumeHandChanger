import cv2
import time
import numpy as np
import volumehandchanger.HandTrackingModule as htm
import math
import pulsectl

#parameters
WCam, HCam = 500, 500

cap = cv2.VideoCapture(0)
cap.set(3, WCam)
cap.set(4, HCam)
PTime = 0

#detector settings
detector = htm.handDetector(model_path="src/data/hand_landmarker.task", detectionCon=0.7)
pulse = pulsectl.Pulse('volume-control')
#sink = pulse.sink_list()[0]

def get_default_sink():
    name = pulse.server_info().default_sink_name
    return pulse.get_sink_by_name(name)

sink = get_default_sink()
current_vol = 0

while True:
    new_sink = get_default_sink()
    if new_sink.index != sink.index:
        sink = new_sink

    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img)
    LMList = detector.findPosition(img, draw=False)

    if len(LMList) != 0:
        x1, y1 = LMList[4][1], LMList[4][2]
        x2, y2 = LMList[8][1], LMList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 12, (161, 1, 166), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (161, 1, 166), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 1, 2), 2)
        cv2.circle(img, (cx, cy), 12, (255, 56, 78), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        vol_norm = np.clip((length - 20) / 200, 0.0, 1.0)
        pulse.volume_set_all_chans(sink, vol_norm)
        current_vol = int(pulse.volume_get_all_chans(sink) * 100)

    CTime = time.time()
    fps = 1 / (CTime - PTime)
    PTime = CTime

    cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (112, 125, 205), 2)

    bar_x = WCam + 80
    bar_y_top = 50
    bar_height = HCam - 100
    bar_width = 40

    cv2.rectangle(img,
                  (bar_x, bar_y_top),
                  (bar_x + bar_width, bar_y_top + bar_height),
                  (0, 0, 0), 3)

    level_px = int(bar_height * (current_vol / 100))

    cv2.rectangle(img,
                  (bar_x, bar_y_top + bar_height - level_px),
                  (bar_x + bar_width, bar_y_top + bar_height),
                  (12, 240, 137), cv2.FILLED)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
