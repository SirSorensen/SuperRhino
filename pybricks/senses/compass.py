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
        return self.imu.heading() - self.heading_threshold

    def calc_error(self, correct_angle) -> float:
        return Trigonometry.calc_diff(self.direction(), correct_angle)

    def angle_needs_correcting(self, correct_angle):
        error = self.calc_error(correct_angle)
        return self.heading_threshold < error

