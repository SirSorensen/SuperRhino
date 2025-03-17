from pybricks._common import IMU
from utils.calibrations import avg_measure
from utils.angle import Angle
from pybricks.parameters import Axis

class Sense_of_Direction:
    def __init__(self, imu : IMU):
        self.imu : IMU = imu
        # Calibrate IMU
        while not self.imu.ready():
            pass