from robot_eyes import RobotEyes
from robot_legs import RobotLegs
from pybricks.parameters import Port
from pybricks.hubs import PrimeHub


class Robot:
    def __init__(self):
        # Initialise Motors (wheels)
        self.legs : RobotLegs = RobotLegs(Port.A, Port.E)

        # Initialize & calibrate the sensors
        self.eyes : RobotEyes = RobotEyes(Port.B, Port.F)

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)

    def test_turn(self):
        self.legs.turn(360)

    def test_forward(self):
        self.prime_hub.imu.reset_heading(180)
        start_heading = 180

        while True:
            self.legs.go_forward()

            if abs(start_heading - self.prime_hub.imu.heading()) > 10:
                self.legs.hold()
                self.legs.turn(start_heading - self.prime_hub.imu.heading())

            print("My eyes see:", self.eyes.what_do_you_see())