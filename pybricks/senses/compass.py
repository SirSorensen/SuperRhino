from pybricks._common import IMU
from utils.calibrations import avg_measure
from senses.utils.angle import Angle

class Compass:
    def __init__(self, imu: IMU):
        self.imu: IMU = imu
        # Calibrate IMU
        while not self.imu.ready():
            pass

        # Calibrations:
        self.reset()
        self.heading_errors = []
        self.heading_threshold = 0

    def direction(self) -> float:
        """Return a float between -179 and 180 which is based on calibrated threshold."""
        return Angle.to_angle(self.imu.heading() - self.heading_threshold)

    def reset(self):
        self.imu.reset_heading(0)

    def is_direction_correct(self, correct_direction):
        error = Angle.calc_error(correct_direction, self.imu.heading())

        if Angle.in_diff_domains(self.heading_threshold, error):
            return False

        return self.heading_threshold >= error

    def calc_direction_error(self, correct_direction):
        if self.is_direction_correct(correct_direction):
            return 0
        else:
            return Angle.calc_error(correct_direction, self.direction())


    ########################## Calibrations: ##########################

    def add_heading_error(self, current_degree) -> float:
        measured_angle = Angle.to_angle(avg_measure(self.imu.heading))
        current_angle = Angle.to_angle(current_degree)
        # If i.e. current_angle = 179 and measure_angle = -179
        error = Angle.calc_error(current_angle, measured_angle)
        self.heading_errors.append(error)

    def finish_calibrate_heading(self):
        avg_heading_error = sum(self.heading_errors) / len(self.heading_errors)
        max_heading_error = max(self.heading_errors)
        self.heading_threshold = Angle.to_angle((avg_heading_error + max_heading_error) / 2)
