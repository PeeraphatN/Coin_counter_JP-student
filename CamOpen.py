# If needed, uncomment the next line to install packages
# !pip install opencv-python numpy matplotlib ipywidgets

import sys, platform, os, math, time
import numpy as np
import cv2
import matplotlib.pyplot as plt

# For inline plots in notebooks
print("Python:", sys.version)
print("OpenCV:", cv2.__version__)
print("OS:", platform.platform())

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("⚠️ Cannot open camera. Try changing index (0→1) or run as .py script.")
else:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    print("Press 's' to save coins.jpg, 'q' to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Frame read failed."); break
        cv2.imshow("Camera", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('s'):
            cv2.imwrite("coins.jpg", frame)
            print("Saved: coins.jpg")
        if k == ord('q'):
            break
    cap.release(); cv2.destroyAllWindows()