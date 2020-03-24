# mport binascii

import requests
# import json
import cv2
import io
import time as Time
import matplotlib.pyplot as plt
# import numpy as np
cap = cv2.VideoCapture("sample/videoplayback.mp4")
fourcc = cv2.VideoWriter_fourcc(*'avc1')

recordCount = 0
faces = ''
while True:
    ret, frame = cap.read()
    if recordCount == 0:
        out = cv2.VideoWriter('test.mp4', fourcc, 20.0, (frame.shape[1], frame.shape[0]))
    recordCount += 1
    out.write(frame)
    if recordCount > 1000:
        out.release()
        break
cap.release()
