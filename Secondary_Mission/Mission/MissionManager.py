# from Secondary_Mission.ImageProcessing import (ClassifyTile, CalculateDanger)
from Secondary_Mission.Camera import CameraObj
from Secondary_Mission.ImageProcessing import VisionSystem
from Secondary_Mission.Sensor import BMEReader
from Secondary_Mission.Sensor import IMUReader
from Secondary_Mission.Sensor import GPSReader
from Secondary_Mission.Radio import RF4463
from Secondary_Mission.Radio import RADIO_CONFIG
import time
import cv2
import numpy as np

path = "Secondary_Mission/ImageProcessing/model.pth"
class MissionManagerObj:
    def __init__(self):
        self.vision = VisionSystem(path)
        self.cameraObj = CameraObj()
        self.bme = BMEReader()
        self.imu = IMUReader()
        self.gps = GPSReader()
        self.imu.Calibrate()
        self.radio = RF4463()
    def run(self):
        while True:
            print(self.imu.ReadSensorData())
            print(self.bme.ReadSensorData())
            print(self.gps.ReadSensorData())
            classes = self.vision.ProcessImage(self.cameraObj.CapturePhoto())
            print(f"Calculated Dangers:{self.vision.CalculateDanger(classes)}")
    # def ClassifyTile(self):
    #     img = cv2.imread("1.png")
    #     print(img.shape)
    #     print(img)
    #     classes = self.vision.ProcessImage(img)
    #     print(classes)
    #     print(self.vision.CalculateDanger(classes))
    def TestRadio(self):
        self.radio.Reset()
        self.radio.PowerUp()
        self.radio.LoadConfig(RADIO_CONFIG)
        time.sleep(0.1)
        while True:
            self.radio.get_state()
            time.sleep(0.5)
            self.radio.write_tx_fifo("l")
            self.radio.start_tx()
            time.sleep(0.1)