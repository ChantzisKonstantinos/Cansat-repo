import spidev
import RPi.GPIO as GPIO
import time

RESET_PIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(RESET_PIN, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
spi.mode = 0


def reset():
    GPIO.output(RESET_PIN, 0)
    time.sleep(0.01)
    GPIO.output(RESET_PIN, 1)
    time.sleep(0.02)


def wait_cts():
    while True:
        resp = spi.xfer2([0x44, 0x00])
        if resp[1] == 0xFF:
            break
        time.sleep(0.001)


def send_cmd(cmd):
    spi.xfer2(cmd)
    wait_cts()


def read_response(n):
    resp = spi.xfer2([0x44] + [0x00]*n)
    return resp[1:]


reset()

# POWER_UP
send_cmd([0x02, 0x01, 0x00, 0x01])

print("POWER_UP sent")

# GET_INT_STATUS
send_cmd([0x20, 0x00, 0x00, 0x00])
resp = read_response(8)

print("INT STATUS:", resp)