# mport binascii

import requests
# import json
import cv2
import io
import time as Time
import matplotlib.pyplot as plt
# import numpy as np
class face_api_ms:
    def __init__(self):
        print('face api init')

    def process_mov(self, mov):
        EMOTIONS = ["neutral", "sadness", "what", "contempt", "happiness", "surprise", "disgust", "some", "fear",
                    "anger"]

        # imoji list return
        def get_imojis():
            s_img = cv2.imread("models/emoji-set.png", -1)
            imoji_images = []
            t_start = 150
            l_start = 41
            item_h = 150
            item_w = 143

            for i in range(1, 3):
                for j in range(1, 6):
                    x = (j - 1) * item_w + l_start
                    y = (i - 1) * item_h + t_start
                    w = j * item_w + l_start
                    h = i * item_h + t_start
                    imoji_images.append(s_img[y:h, x:w])
            return imoji_images

        imojis = get_imojis()

        # 사용자 아이디와 시리얼 넘버로 된 파일명 변경 필요
        time = Time.time()
        time = str(int(time))

        mov.save("fileserver/input/" + time + ".mp4")
        cap = cv2.VideoCapture("fileserver/input/" +  time + ".mp4")
        # mov.save("C:\\projectWork\\2.reactNative\\flaskRestful\\\sample\\" + time + ".mp4")
        # cap = cv2.VideoCapture("C:\\projectWork\\2.reactNative\\flaskRestful\\\sample\\" +  time + ".mp4")
        fourcc = cv2.VideoWriter_fourcc(*'H264')

        recordCount = 0
        faces = ''
        while True:
            ret, frame = cap.read()

            if recordCount == 0:
                out = cv2.VideoWriter('fileserver/output/' + time + '.mp4', fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                # out = cv2.VideoWriter('C:\\projectWork\\2.reactNative\\flaskRestful\\\sample\\output.mp4', fourcc, 20.0, (frame.shape[1], frame.shape[0]))
            recordCount += 1

            if recordCount < 500:
                continue

            if recordCount % 20 == 0:
                buf = io.BytesIO()
                plt.imsave(buf, frame, format='jpeg')
                image_data = buf.getvalue()

                face_uri = "http://52.141.7.91:8500/face/v1.0/detect?returnFaceAttributes=*"
                headers = {"Content-Type": "image/jpeg"}
                response = requests.post(face_uri, headers=headers, data=image_data)

                faces = response.json()
                print(recordCount)

            for ret_face in faces:
                x = ret_face["faceRectangle"]['left']
                y = ret_face["faceRectangle"]['top']
                w = ret_face["faceRectangle"]['width']
                h = ret_face["faceRectangle"]['height']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                ret_emotion = ret_face["faceAttributes"]["emotion"]
                max_emotion = max(ret_emotion.keys(), key=(lambda k: ret_emotion[k]))
                imoji_index = 0
                if max_emotion in EMOTIONS:
                    imoji_index = EMOTIONS.index(max_emotion)
                add_imoji = imojis[imoji_index]

                y2 = y + add_imoji.shape[0]
                x2 = x + add_imoji.shape[1]

                alpha_s = add_imoji[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s

                for c in range(0, 3):
                    frame[y:y2, x:x2, c] = (alpha_s * add_imoji[:, :, c] + alpha_l * frame[y:y2, x:x2, c])
                    emoframe = frame

                    # cv2.imshow("Probabilities", frame)
                    # cv2.waitKey(0)
            out.write(emoframe)
            # imagefilename = 'fer2013/face_sample.jpg'
            # image = cv2.imread(imagefilename)
            #
            # with open(imagefilename, 'rb') as f:
            #     data = f.read()

            if recordCount > 1000:
                out.release()
                break
        cap.release()

        return "Done", str(int(time)) + ".mp4"

