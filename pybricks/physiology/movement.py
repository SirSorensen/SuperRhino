from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase


class Movement:
    def __init__(
                 self, left_motor_port: Port, right_motor_port: Port,
                 wheel_diameter=56, axle_track=160,
                 _turn_rate=50, _turn_degree=40, _speed=400
                ):
        # Initialise Motors (wheels)
        self.left_motor: Motor = Motor(left_motor_port, Direction.COUNTERCLOCKWISE)
        self.right_motor: Motor = Motor(right_motor_port)

        self.drive_base: DriveBase = DriveBase(self.left_motor, self.right_motor, wheel_diameter=wheel_diameter, axle_track=axle_track)

        self.turn_rate = _turn_rate
        self.turn_degree = _turn_degree
        self.speed = _speed

    def turn_degrees(self, degrees):
        angle = degrees
        self.drive_base.turn(angle)
