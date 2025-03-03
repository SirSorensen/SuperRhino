
from pybricks.pupdevices import ColorSensor
import calibrations as cal

class RobotEyes:
    def __init__(self, left_port, right_port):
        # Initialize & calibrate the sensors.
        self.left_sensor: ColorSensor = ColorSensor(left_port)
        self.left_threshold = cal.calibrate_light_sensor(self.left_sensor)

        self.right_sensor: ColorSensor = ColorSensor(right_port)
        self.right_threshold = cal.calibrate_light_sensor(self.right_sensor)

    def what_do_you_see(self):
        return (self.left_sensor.reflection(), self.right_sensor.reflection())
