from Secondary_Mission.ImageProcessing import (ClassifyTile, CalculateDanger)
from Secondary_Mission.Camera import CameraObj
from Secondary_Mission.ImageProcessing import VisionSystem

path = "Secondary_Mission/ImageProcessing/model.pth"
class MissionManagerObj:
    def __init__(self):
        self.vision = VisionSystem(path)
        self.cameraObj = CameraObj()
        # print("cam init",self.cameraObj)
        # bme = BMEReader()
        # print("bme init",bme)
    def pnb(self):
        # print(bme.ReadSensorData())
        print(self.vision.ProcessImage(self.cameraObj.CapturePhoto()))