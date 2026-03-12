import serial
import pynmea2

ser = serial.Serial('/dev/serial0', 9600, timeout=1)

while True:
    line = ser.readline().decode('ascii', errors='ignore')
    if line.startswith('$GPGGA'):
        msg = pynmea2.parse(line)
        print(
            "Fix:", msg.gps_qual,
            "Satellites:", msg.num_sats,
            "Lat:", msg.latitude,
            "Lon:", msg.longitude
        )