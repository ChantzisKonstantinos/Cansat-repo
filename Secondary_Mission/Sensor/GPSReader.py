import pynmea2
import serial

class GPSReader:
    def __init__(self):
        self.ser = serial.Serial('/dev/serial0', 9600, timeout=0.1)
    def ReadSensorData(self):
        while True:
            line = self.ser.readline().decode('ascii', errors='ignore')
            if not line:
                break
            if line.startswith('$GPGGA'):
                gpsData = pynmea2.parse(line)
                # msg = f"Fix: {gpsData.gps_qual}\nSatellites: {gpsData.num_sats}\nLatitude: {gpsData.latitude:.4f}\nLongitude: {gpsData.longitude:.4f}"
                msg = f"Latitude: {gpsData.latitude:.4f} Longitude: {gpsData.longitude:.4f}"
                return msg








# ser = serial.Serial('/dev/serial0', 9600, timeout=1)

# while True:
#     line = ser.readline().decode('ascii', errors='ignore')
#     if line.startswith('$GPGGA'):
#         msg = pynmea2.parse(line)
#         print(
#             "Fix:", msg.gps_qual,
#             "Satellites:", msg.num_sats,
#             "Lat:", msg.latitude,
#             "Lon:", msg.longitude
#         )