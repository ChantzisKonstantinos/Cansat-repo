import board
import adafruit_tcs34725
import time
class RGBSensor:
    def __init__(self):
        self.i2c = board.I2C()
        self.sensor = adafruit_tcs34725.TCS34725(self.i2c)
    def read_color(self):
        color = self.sensor.color
        color_rgb = self.sensor.color_rgb_bytes
        temp = self.sensor.color_temperature
        lux = self.sensor.lux
        return color, color_rgb, temp, lux