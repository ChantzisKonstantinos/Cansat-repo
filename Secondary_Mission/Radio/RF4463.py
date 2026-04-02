import spidev
import RPi.GPIO as GPIO
import time

class RF4463:
    def __init__(self, bus=0, device=0, nirq=25, sdn=24):
        self.NIRQ = nirq
        self.SDN = sdn

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.NIRQ, GPIO.IN)
        GPIO.setup(self.SDN, GPIO.OUT)

        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0

    def SendCmd(self, cmd):
        return self.spi.xfer2(cmd)

    def wait_cts(self):
        while True:
            resp = self.spi.xfer2([0x44, 0x00])
            if resp[1] == 0xFF:
                break
            time.sleep(0.001)

    def Reset(self):
        GPIO.output(self.SDN, 1)
        time.sleep(0.1)
        GPIO.output(self.SDN, 0)
        time.sleep(0.1)

    def PowerUp(self):
        """Basic POWER_UP command"""
        self.wait_cts()
        self.SendCmd([0x02, 0x81, 0x00, 0x01, 0xC9, 0xC3, 0x80])
        time.sleep(0.05)

    def LoadConfig(self, config):
        for cmd in config:
            self.wait_cts()
            self.SendCmd(cmd)
            time.sleep(0.01)

    def write_tx_fifo(self, data):
        payload = list(data.encode())
        self.wait_cts()
        # self.SendCmd([0x66] + payload)
        self.spi.xfer2([0x66] + [0xAA]*64)
    def start_tx(self):
        self.wait_cts()
        self.SendCmd([
            0x31,       # start TX
            0x00,       # channel
            0x30,       # TX immediately
            0x40, 0x00 
        ])

    def send_packet(self, data):
        print("Sending:", data)
        self.write_tx_fifo(data)
        self.start_tx()
    def get_state(self):
        self.SendCmd([0x33])
        self.wait_cts()
        resp = self.spi.xfer2([0x44, 0x00, 0x00])
        print("RAW RESP:", resp)
        cts = hex(resp[1])
        state = hex(resp[2])
        print("cts:", cts, "state:", state)

    def close(self):
        self.spi.close()
        GPIO.cleanup()