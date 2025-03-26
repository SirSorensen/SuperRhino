from utils.trigonometry import Trigonometry


class Compass:
    def __init__(self, imu):
        self.imu = imu
        # Calibrate IMU
        while not self.imu.ready():
            pass

        # Calibrations:
        self.imu.reset_heading(0)
        self.heading_threshold = 0.9061487

    def direction(self) -> float:
        """Return a float between 0 and 360 which is based on calibrated threshold."""
        h = (self.imu.heading() - (self.heading_threshold/2))
        while h < 0:
            h += 360
        return h % 360

    def calc_error(self, correct_angle) -> float:
        return Trigonometry.calc_diff(self.direction(), correct_angle)

    def angle_needs_correcting(self, correct_angle, sensitivity = 1):
        error = self.calc_error(correct_angle)
        return abs(error) > abs(self.heading_threshold * sensitivity)

