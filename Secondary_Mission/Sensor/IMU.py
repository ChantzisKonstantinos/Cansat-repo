import smbus
import time
import math

MPU_ADDR = 0x68

PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# constants
G = 9.80665

# default sensor scales
ACCEL_SCALE = 16384.0   # LSB/g for ±2g
GYRO_SCALE = 131.0      # LSB/(deg/s) for ±250 deg/s

class IMUReader:
    def __init__(self, address=0x68):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)
    def ReadWord(self, reg):
        high = self.bus.read_byte_data(MPU_ADDR, reg)
        low = self.bus.read_byte_data(MPU_ADDR, reg + 1)
        value = (high << 8) | low
        if value >= 0x8000:
            value -= 65536
        return value
    def Calibrate(self, samples=500):
        gx_sum = gy_sum = gz_sum = 0
        ax_sum = ay_sum = az_sum = 0

        for _ in range(samples):
            gx_sum += self.ReadWord(GYRO_XOUT_H)
            gy_sum += self.ReadWord(GYRO_XOUT_H + 2)
            gz_sum += self.ReadWord(GYRO_XOUT_H + 4)
            ax_sum += self.ReadWord(ACCEL_XOUT_H)
            ay_sum += self.ReadWord(ACCEL_XOUT_H + 2)
            az_sum += self.ReadWord(ACCEL_XOUT_H + 4)
        
        self.acc_bias_x = ax_sum / samples
        self.acc_bias_y = ay_sum / samples
        self.acc_bias_z = az_sum / samples - 16384   # subtract gravity
        self.gyro_bias_x = gx_sum / samples
        self.gyro_bias_y = gy_sum / samples
        self.gyro_bias_z = gz_sum / samples
    def ReadSensorData(self):
        ax_raw = self.ReadWord(ACCEL_XOUT_H)
        ay_raw = self.ReadWord(ACCEL_XOUT_H + 2)
        az_raw = self.ReadWord(ACCEL_XOUT_H + 4)

        gx_raw = self.ReadWord(GYRO_XOUT_H)
        gy_raw = self.ReadWord(GYRO_XOUT_H + 2)
        gz_raw = self.ReadWord(GYRO_XOUT_H + 4)

        ax = ((ax_raw - self.acc_bias_x) / ACCEL_SCALE) * G
        ay = ((ay_raw - self.acc_bias_y) / ACCEL_SCALE) * G
        az = ((az_raw - self.acc_bias_z) / ACCEL_SCALE) * G

        gx = math.radians((gx_raw - self.gyro_bias_x) / GYRO_SCALE)
        gy = math.radians((gy_raw - self.gyro_bias_y) / GYRO_SCALE)
        gz = math.radians((gz_raw - self.gyro_bias_z) / GYRO_SCALE)
        msg = f"Acceleration (m/s^2): {ax:.3f}, {ay:.3f}, {az:.3f}\nAngular vel (rad/s): {gx:.3f}, {gy:.3f}, {gz:.3f}"
        return msg



# # wake up the MPU


# def read_word(reg):
#     high = bus.read_byte_data(MPU_ADDR, reg)
#     low = bus.read_byte_data(MPU_ADDR, reg + 1)

#     value = (high << 8) | low
#     if value >= 0x8000:
#         value -= 65536

#     return value

# samples = 500

# gx_sum = gy_sum = gz_sum = 0
# ax_sum = ay_sum = az_sum = 0

# for _ in range(samples):
#     gx_sum += read_word(GYRO_XOUT_H)
#     gy_sum += read_word(GYRO_XOUT_H + 2)
#     gz_sum += read_word(GYRO_XOUT_H + 4)
#     ax_sum += read_word(ACCEL_XOUT_H)
#     ay_sum += read_word(ACCEL_XOUT_H + 2)
#     az_sum += read_word(ACCEL_XOUT_H + 4)
    
# acc_bias_x = ax_sum / samples
# acc_bias_y = ay_sum / samples
# acc_bias_z = az_sum / samples - 16384   # subtract gravity
# gyro_bias_x = gx_sum / samples
# gyro_bias_y = gy_sum / samples
# gyro_bias_z = gz_sum / samples


# print(acc_bias_x, acc_bias_y, acc_bias_z)
# print(gyro_bias_x, gyro_bias_y, gyro_bias_z)

# while True:

#     # raw accelerometer
#     ax_raw = read_word(ACCEL_XOUT_H)
#     ay_raw = read_word(ACCEL_XOUT_H + 2)
#     az_raw = read_word(ACCEL_XOUT_H + 4)

#     # raw gyro
#     gx_raw = read_word(GYRO_XOUT_H)
#     gy_raw = read_word(GYRO_XOUT_H + 2)
#     gz_raw = read_word(GYRO_XOUT_H + 4)

#     # convert to SI
#     ax = ((ax_raw - acc_bias_x) / ACCEL_SCALE) * G
#     ay = ((ay_raw - acc_bias_y) / ACCEL_SCALE) * G
#     az = ((az_raw - acc_bias_z) / ACCEL_SCALE) * G

#     gx = math.radians((gx_raw - gyro_bias_x) / GYRO_SCALE)
#     gy = math.radians((gy_raw - gyro_bias_y) / GYRO_SCALE)
#     gz = math.radians((gz_raw - gyro_bias_z) / GYRO_SCALE)

#     print(f"Acceleration (m/s^2): {ax:.3f}, {ay:.3f}, {az:.3f}")
#     print(f"Angular vel (rad/s): {gx:.3f}, {gy:.3f}, {gz:.3f}")
#     print()

#     time.sleep(0.5)
#     import time


