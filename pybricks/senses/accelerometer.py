from pybricks._common import IMU
from utils.calibrations import avg_measure
from pybricks.parameters import Axis

class Accelerometer:
    def __init__(self, imu: IMU):
        self.imu: IMU = imu
        # Calibrate IMU
        while not self.imu.ready():
            pass

        # Calibrations:
        self.calibrate_acceleration()


    ########################## Calibrations: ##########################

    def calibrate_acceleration(self) -> dict[str, float]:
        avg_acc_x_stationary = avg_measure(self.imu.acceleration, parameters=Axis.X)
        avg_acc_y_stationary = avg_measure(self.imu.acceleration, parameters=Axis.Y)
        avg_acc_z_stationary = avg_measure(self.imu.acceleration, parameters=Axis.Z)
        acceleration_error_z = 9816 - avg_acc_z_stationary  # Denmark's gravitational acceleration = 9.816 m/s^2 (source: https://lex.dk/tyngdeacceleration#:~:text=Tyngdeaccelerationen%20i%20Danmark%20er%209%2C816%20m%2Fs%C2%B2.)
        self.acceleration_error = {"X": avg_acc_x_stationary, "Y": avg_acc_y_stationary, "Z": acceleration_error_z}