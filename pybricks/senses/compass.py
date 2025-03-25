from pybricks._common import IMU

class Compass:
    def __init__(self, imu: IMU):
        self.imu: IMU = imu
        # Calibrate IMU
        while not self.imu.ready():
            pass