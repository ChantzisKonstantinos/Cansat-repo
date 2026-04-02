from picamera2 import Picamera2
from libcamera import Transform
from PIL import Image
import time

class CameraObj:
    def __init__(self):
        self.cam = Picamera2()
        self.cameraConfig = self.cam.create_still_configuration(
            main={"size": (1024, 1024)}
            )
        self.cam.configure(self.cameraConfig)
        self.cam.start()
        time.sleep(1)
    def CapturePhoto(self):
        image = self.cam.capture_array()
        img = Image.fromarray(image)
        img.save("angel.jpg", format="JPEG")
        return image
    def StopCamera(self):
        self.cam.stop()

# newCam = CameraObj()
# newCam.CapturePhoto("a")
# from picamera2 import Picamera2
# from libcamera import Transform
# from PIL import Image
# import time

# cam = Picamera2()
# def ConfigureCamera():
#     cameraConfig = cam.create_still_configuration(
#     main={"size": (1024, 1024)}
#     )
#     cam.configure(cameraConfig)

# def StartCamera(startDelay):
#     cam.start()
#     time.sleep(startDelay)
# def StopCamera():
#     cam.stop()


# def CapturePhoto(picName):
#     image = cam.capture_array()
#     img = Image.fromarray(image)
#     img.save(picName, format="JPEG")
# ConfigureCamera()
# StartCamera(1)
# CapturePhoto("a")
# StopCamera()
