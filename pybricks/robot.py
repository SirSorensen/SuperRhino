import calibrations as cal
from robot_eyes import RobotEyes
from robot_legs import RobotLegs

from pybricks.hubs import PrimeHub
from pybricks.parameters import Port


class Robot:
    def __init__(self):
        # Initialise Motors (wheels)
        self.legs : RobotLegs = RobotLegs(Port.A, Port.E)

        # Initialize & calibrate the sensors
        self.eyes : RobotEyes = RobotEyes(Port.B, Port.F)

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)

        # Calibrate acceleration:
        self.acceleration_error = cal.calibrate_acceleration(self)