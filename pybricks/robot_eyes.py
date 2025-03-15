
from pybricks.pupdevices import ColorSensor
import calibrations as cal

class RobotEyes:
    def __init__(self, left_port, right_port):
        # Initialize & calibrate the sensors.
        self.left_sensor: ColorSensor = ColorSensor(left_port)
        self.left_threshold = cal.calibrate_light_sensor(self.left_sensor)

        self.right_sensor: ColorSensor = ColorSensor(right_port)
        self.right_threshold = cal.calibrate_light_sensor(self.right_sensor)

        self.cliff_acc = 0
        self.do_I_see_a_tape = (False, False)

    def measure(self):
        left = self.left_sensor.reflection()
        right = self.right_sensor.reflection()

        if left <= 5 or right <= 5:
            self.cliff_acc += 1
        elif self.cliff_acc > 0:
            self.cliff_acc -= 1

        self.do_I_see_tape = ((10 <= left <= 15), (10 <= right <= 15))

        return (left, right)


    def do_I_see_a_cliff(self):
        return  self.cliff_acc > 150
