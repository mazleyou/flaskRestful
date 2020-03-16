import face_api_ms
from werkzeug.datastructures import FileStorage
file = None

with open('sample/videoplayback.mp4', 'rb') as fp:
    file = FileStorage(fp)

faceapi = face_api_ms.face_api_ms()
ret = faceapi.process_mov(file)