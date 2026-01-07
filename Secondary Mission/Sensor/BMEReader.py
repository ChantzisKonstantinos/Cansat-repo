import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

i2c = busio.I2C(board.SCL, board.SDA)
bme = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

groundAltitude = 1013.25
readRate = 0.5

def AltitudeConverter(pres):
    return 44330*(1-(pres/groundAltitude)**0.1903)
try:
    while True:
        print("Temperature: {:.3f} °C".format(bme.temperature))
        print("Humidity:    {:.3f} %".format(bme.humidity))
        print("Pressure:    {:.3f} hPa".format(bme.pressure))
        print("Altitude:    {:.3f} meters".format(AltitudeConverter(bme.pressure)))
        print("-" * 30)
        time.sleep(readRate)


except KeyboardInterrupt:
    print("STOP")