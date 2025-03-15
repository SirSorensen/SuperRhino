# Hardware of Vehicle 1:
#     Excitatory sensor directly coupled to motor
#     Motor speed controlled by sensor
#
# Behavior of Vehicle 1:
#     Motion always forward
#     Motion speed depends on light intensity
#     Changes in direction from environmental perturbations (slippage, rough terrain)

class Vehicle_1:
    def __init__(
                 self,
                 motor_1, sensor_1
                ):
        self.motor_1 = motor_1
        self.sensor_1 = sensor_1

    def run(self):
        while True:
            self.motor_1(100)