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
        self.legs : RobotLegs = RobotLegs(Port.B, Port.A)

        # Initialize & calibrate the sensors
        # We currently have no eyes
        #self.eyes : RobotEyes = RobotEyes(Port.B, Port.F)

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)


