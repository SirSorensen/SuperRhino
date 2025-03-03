
import calibrations as cal
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase


class RobotLegs:
    def __init__(self, left_port : Port, right_port : Port):
        # Initialise Motors (wheels)
        self.left_motor: Motor = Motor(left_port, Direction.COUNTERCLOCKWISE)
        self.right_motor: Motor = Motor(right_port)

        self.drive_base: DriveBase = DriveBase(self.left_motor, self.right_motor,
                                               wheel_diameter=56, axle_track=160
                                               )

        self.turn_rate = 50
        self.turn_degree = 40
        self.speed = 200

    def go_forward(self):
        self.left_motor.run(self.speed)
        self.right_motor.run(self.speed)

    def go_back(self):
        self.left_motor.run(-self.speed)
        self.right_motor.run(-self.speed)

    def hold(self):
        self.left_motor.hold()
        self.right_motor.hold()

    def turn(self, angle):
        self.drive_base.turn(angle)