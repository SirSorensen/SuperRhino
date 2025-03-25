from pybricks._common import IMU
from utils.trigonometry import Trigonometry
from utils.calibrations import avg_measure


class Compass:
    def __init__(self, imu: IMU):
        self.imu: IMU = imu
        # Calibrate IMU
        while not self.imu.ready():
            pass

        # Calibrations:
        self.imu.reset_heading(0)
        self.heading_errors = []
        self.heading_threshold = 0

    def direction(self) -> float:
        """Return a float between 0 and 360 which is based on calibrated threshold."""
        return self.imu.heading() - self.heading_threshold

    ########################## Calibrations: ##########################

    def add_heading_error(self, current_degree) -> float:
        measured_angle = avg_measure(self.imu.heading)
        current_angle = current_degree
        # If i.e. current_angle = 3 and measure_angle = 357
        error = Trigonometry.calc_diff(current_angle, measured_angle)
        self.heading_errors.append(error)

    def finish_calibrate_heading(self):
        avg_heading_error = sum(self.heading_errors) / len(self.heading_errors)
        max_heading_error = max(self.heading_errors)
        self.heading_threshold = (avg_heading_error + max_heading_error) / 2
