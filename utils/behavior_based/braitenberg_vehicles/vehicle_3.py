# Hardware of Vehicle 3:
#     Two inhibitory sensor directly coupled to two motors
#
# Behavior of Vehicle 3:
#     Slow down when strong stimulus
#     Speed up when weak stimulus
#     Both “likes” the source (slower when near)
#     “Love” of light (stops and stares)
#     “Explores” world

class Vehicle_3:
    def __init__(
                 self,
                 motor_left,  sensor_left,
                 motor_right, sensor_right
                ):
        self.motor_left = motor_left
        self.sensor_left = sensor_left
        self.motor_right = motor_right
        self.sensor_right = sensor_right

    def run_lover(self):
        while True:
            self.motor_left(100-self.sensor_left())
            self.motor_right(100-self.sensor_right())

    def run_explorer(self):
        while True:
            self.motor_left(100-self.sensor_right())
            self.motor_right(100-self.sensor_left())