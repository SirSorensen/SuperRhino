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

        # Calibrations:
        self.calibrate_acceleration()
        self.heading_errors = []
        self.heading_threshold = 0


    def direction(self) -> float:
        """Return a float between -179 and 180 which is based on calibrated threshold."""
        return Angle.to_angle(self.imu.heading() - self.heading_threshold)


    ########################## Calibrations: ##########################

    def calibrate_acceleration(self) -> dict[str, float]:
        avg_acc_x_stationary = avg_measure(self.imu.acceleration, parameters=Axis.X)
        avg_acc_y_stationary = avg_measure(self.imu.acceleration, parameters=Axis.Y)
        avg_acc_z_stationary = avg_measure(self.imu.acceleration, parameters=Axis.Z)
        acceleration_error_z = 9816 - avg_acc_z_stationary # Denmark's gravitational acceleration = 9.816 m/s^2 (source: https://lex.dk/tyngdeacceleration#:~:text=Tyngdeaccelerationen%20i%20Danmark%20er%209%2C816%20m%2Fs%C2%B2.)
        self.acceleration_error = {"X": avg_acc_x_stationary, "Y": avg_acc_y_stationary, "Z": acceleration_error_z}

    def add_heading_error(self, current_degree) -> float:
        measure_angle = Angle.to_angle(avg_measure(self.imu.heading))
        current_angle = Angle.to_angle(current_degree)
        # If i.e. current_angle = 179 and measure_angle = -179
        if (current_angle >= 0 > measure_angle or measure_angle >= 0 > current_angle) and (abs(current_angle) > 100 and abs(measure_angle) > 100):
            print(f"({current_angle} >= 0 > {measure_angle} or {measure_angle} >= 0 > {current_angle}) = True" )
            if current_angle >= 0 > measure_angle:
                error = current_degree - (measure_angle + 360)
            else:
                error = current_degree - (measure_angle - 360)
        else:
            error = current_degree - measure_angle

        self.heading_errors.append(error)

    def finish_calibrate_heading(self):
        avg_heading_error = sum(self.heading_errors) / len(self.heading_errors)
        max_heading_error = max(self.heading_errors)
        self.heading_threshold = (avg_heading_error + max_heading_error) / 2
