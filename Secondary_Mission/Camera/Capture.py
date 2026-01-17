from picamera2 import Picamera2
from libcamera import Transform
from PIL import Image
import time

cam = Picamera2()
def ConfigureCamera():
    cameraConfig = cam.create_still_configuration(
    main={"size": (1024, 1024)}
    )
    cam.configure(cameraConfig)

def StartCamera(startDelay):
    cam.start()
    time.sleep(startDelay)
def StopCamera():
    cam.stop()


def CapturePhoto(picName):
    image = cam.capture_array()
    img = Image.fromarray(image)
    img.save(picName, format="JPEG")

