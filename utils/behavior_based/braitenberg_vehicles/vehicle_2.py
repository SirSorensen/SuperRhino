# Hardware of Vehicle 2:
#     Two excitatory sensor directly coupled to two motors (differential-drive wheels)
#
# Behavior of Vehicle 2:
#     “Coward”, it has fear of light source
#     “Aggressive” toward light source

class Vehicle_2:
    def __init__(
                 self,
                 motor_left,  sensor_left,
                 motor_right, sensor_right
                ):
        self.motor_left = motor_left
        self.sensor_left = sensor_left
        self.motor_right = motor_right
        self.sensor_right = sensor_right

    def run_coward(self):
        while True:
            self.motor_left(self.sensor_left())
            self.motor_right(self.sensor_right())

    def run_aggressive(self):
        while True:
            self.motor_left(self.sensor_right())
            self.motor_right(self.sensor_left())