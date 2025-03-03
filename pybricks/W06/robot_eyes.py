
from pybricks.pupdevices import ColorSensor
import calibrations as cal

class RobotEyes:
    def __init__(self, left_port, right_port):
        # Initialize & calibrate the sensors.
        self.left_sensor: ColorSensor = ColorSensor(left_port)
        self.left_threshold = cal.calibrate_light_sensor(self.left_sensor)

        self.right_sensor: ColorSensor = ColorSensor(right_port)
        self.right_threshold = cal.calibrate_light_sensor(self.right_sensor)

    def go_forward(self):
        pass  # TODO

    def go_back(self):
        pass  # TODO

    def turn(self, angle):
        pass  # TODO
