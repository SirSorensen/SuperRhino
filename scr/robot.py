from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.robotics import DriveBase

class Robot:
    def __init__(self):
        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()

        # Initialise Motors (wheels)
        self.left_motor: Motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
        self.right_motor: Motor = Motor(Port.A)

        # Initialise Motors (wheels)
        wheel_diameter=56
        axle_track=85,
        self.drive_base: DriveBase = DriveBase(self.left_motor, self.right_motor, wheel_diameter=wheel_diameter, axle_track=axle_track)

        # Initialize sensors
        self.left_sensor: ColorSensor = ColorSensor(Port.F)
        self.left_sensor.lights.on()
        self.right_sensor: ColorSensor = ColorSensor(Port.E)
        self.right_sensor.lights.on()