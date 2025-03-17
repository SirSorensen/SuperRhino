from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase


class Movement:
    def __init__(self, left_motor_port: Port, right_motor_port: Port, wheel_diameter=56, axle_track=85, turn_rate=50, turn_degree=40, speed=200):
        # Initialise Motors (wheels)
        self.left_motor: Motor = Motor(left_motor_port, Direction.COUNTERCLOCKWISE)
        self.right_motor: Motor = Motor(right_motor_port)

        self.drive_base: DriveBase = DriveBase(self.left_motor, self.right_motor, wheel_diameter=wheel_diameter, axle_track=axle_track)

        self.turn_rate = turn_rate
        self.turn_degree = turn_degree
        self.speed = speed

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

    def reset_distance(self):
        self.drive_base.reset()

    def get_distance(self):
        return self.drive_base.distance()

    def spin(self):
        self.drive_base.turn(360)
