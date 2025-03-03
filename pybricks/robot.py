from robot_eyes import RobotEyes
from robot_legs import RobotLegs
from pybricks.parameters import Port


class Robot:
    def __init__(self):
        # Initialise Motors (wheels)
        self.legs : RobotLegs = RobotLegs(Port.A, Port.E)

        # Initialize & calibrate the sensors
        self.eyes : RobotEyes = RobotEyes(Port.B, Port.F)

    def test_turn(self):
        self.legs.turn(360, self.prime_hub.imu)

    def test_forward(self):
        self.legs.go_forward()