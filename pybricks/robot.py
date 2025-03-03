from robot_eyes import RobotEyes
from robot_legs import RobotLegs
from pybricks.parameters import Port
from pybricks.hubs import PrimeHub
from pybricks.tools import wait


class Robot:
    def __init__(self):
        ### Measurements ###
        # About 8 cm from eye to leg

        # Initialise Motors (wheels)
        self.legs : RobotLegs = RobotLegs(Port.A, Port.E)

        # Initialize & calibrate the sensors
        self.eyes : RobotEyes = RobotEyes(Port.B, Port.F)

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)

    def test_turn(self):
        self.legs.turn(360)

    def test_eyes(self):
        while True:
            print(self.eyes.measure())

    def test_forward(self):
        self.prime_hub.imu.reset_heading(180)
        start_heading = 180

        while True:
            self.legs.go_forward()
            eyes_left, eyes_right = self.eyes.measure()

            if abs(start_heading - self.prime_hub.imu.heading()) > 10:
                self.legs.hold()
                self.legs.turn(start_heading - self.prime_hub.imu.heading())
            if self.eyes.do_I_see_a_cliff():
                print("I see a cliff!")
                self.legs.hold()
                self.legs.go_back()
                wait(1000)
                self.legs.turn(90)
                self.prime_hub.imu.reset_heading(180)

            if self.eyes.do_I_see_tape:
                print("I see tape!")

