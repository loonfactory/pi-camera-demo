# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import cv2
from PIL import Image
from io import BytesIO
from flask import Flask, Response, send_file
from CameraService import CameraService

save_path = 'recode'

app = Flask(__name__)
cap = CameraService(0)
cap.start()

PAGE = """\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""


@app.route("/")
def hello_world():
    return PAGE


def cameraRead(camera):
    while True:
        frame = camera.read()
        if frame is not None:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            jpg = Image.fromarray(imgRGB)
            content = BytesIO()
            jpg.save(content, 'JPEG')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + content.getvalue() + b'\r\n')


@app.route('/stream.mjpg')
def stream():
    response = Response(cameraRead(cap),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return response


@app.route('/recode/<name>')
def recode(name):
    cap.recode(f'{name}.mp4')
    return ('', 204)

@app.route('/save')
def save():
    cap.save()
    return ('', 204)

@app.route('/download/<name>')
def download(name):
    return send_file(f'{save_path}/{name}.mp4', as_attachment=True)

@app.route('/snapshot')
def snapshot():
    frame = cap.read()
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    jpg = Image.fromarray(imgRGB)
    content = BytesIO()
    jpg.save(content, 'JPEG')
    return Response(content.getvalue(), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(threaded=True)
