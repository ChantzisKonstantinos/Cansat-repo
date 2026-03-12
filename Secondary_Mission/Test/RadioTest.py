import spidev
import RPi.GPIO as GPIO
import time

RESET_PIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(RESET_PIN, GPIO.OUT)

# Reset the module
GPIO.output(RESET_PIN, GPIO.LOW)
time.sleep(0.01)
GPIO.output(RESET_PIN, GPIO.HIGH)
time.sleep(0.02)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
spi.mode = 0b00

# 1. POWER_UP command (datasheet: 0x02)
# Arguments: 0x01 (functionality), 0x00 (XO/clock config), 0x01 (boot options)
resp = spi.xfer2([0x02, 0x01, 0x00, 0x01])
print("POWER_UP response:", resp)

# After POWER_UP, wait at least 1ms
time.sleep(0.01)

# 2. Get INT status to confirm chip is alive
resp = spi.xfer2([0x20])
print("INT status:", resp)
