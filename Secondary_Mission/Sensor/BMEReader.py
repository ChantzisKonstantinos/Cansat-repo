import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

class BMEReader:
    def __init__(self, address=0x76):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.bme = adafruit_bme280.Adafruit_BME280_I2C(self.i2c, address=address)
        self.groundAltitude = 1013.25
    def ReadSensorData(self):
        self.altitude = 44330*(1-(self.bme.pressure/self.groundAltitude)**0.1903)
        return altitude, self.bme.temperature, self.bme.humidity, self.bme.pressure
"""try:
    while True:
        print("Temperature: {:.3f} °C".format(bme.temperature))
        print("Humidity:    {:.3f} %".format(bme.humidity))
        print("Pressure:    {:.3f} hPa".format(bme.pressure))
        print("-" * 30)
        time.sleep(readRate)


except KeyboardInterrupt:
    print("STOP")"""