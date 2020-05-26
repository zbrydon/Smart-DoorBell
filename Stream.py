#!/usr/bin/env python
from flask import Flask, render_template, Response, jsonify, request
from pygame import mixer
from PIL import Image
import PIL
from io import BytesIO
from itertools import count
mixer.init()

# emulated camera
from camera import Camera

iid = count()


# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/Hello')
def Hello():
    sound = mixer.Sound('hello.wav')
    sound.play()
    return render_template('index.html')
@app.route('/GoodBye')
def GoodBye():
    sound = mixer.Sound('goodbye.wav')
    sound.play()
    return render_template('index.html')
@app.route('/ComeIn')
def ComeIn():
    sound = mixer.Sound('comein.wav')
    sound.play()
    return render_template('index.html')
@app.route('/LeavePackage')
def LeavePackage():
    sound = mixer.Sound('leavepackage.wav')
    sound.play()
    return render_template('index.html')
@app.route('/GoAway')
def GoAway():
    sound = mixer.Sound('goaway.wav')
    sound.play()
    return render_template('index.html')

@app.route('/TakePicture')

def TakePicture():
    x = next(iid)
    pic = Image.open(BytesIO(Camera.frame))
    pic = pic.save("/home/pi/zbrydon/SmartDoorBell/Media/image%x.jpg" % x )
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)