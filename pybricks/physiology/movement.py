from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from utils.angle import Angle


class Movement:
    def __init__(self, left_motor_port: Port, right_motor_port: Port, wheel_diameter=56, axle_track=85, turn_rate=50, turn_degree=40, speed=400):
        # Initialise Motors (wheels)
        self.left_motor: Motor = Motor(left_motor_port, Direction.COUNTERCLOCKWISE)
        self.right_motor: Motor = Motor(right_motor_port)

        self.drive_base: DriveBase = DriveBase(self.left_motor, self.right_motor, wheel_diameter=wheel_diameter, axle_track=axle_track)

        self._turn_rate = turn_rate
        self._turn_degree = turn_degree
        self._speed = speed

    def go_forward(self):
        self.left_motor.run(self._speed)
        self.right_motor.run(self._speed)

    def go_back(self):
        self.left_motor.run(-self._speed)
        self.right_motor.run(-self._speed)

    def hold(self):
        self.left_motor.hold()
        self.right_motor.hold()

    def turn(self, degree):
        angle = Angle.to_angle(degree)
        self.drive_base.turn(angle)

    def slow_turn(self, dir : Direction):
        if dir.name == Direction.CLOCKWISE:
            self.left_motor.run(self._turn_rate)
            self.right_motor.run(-self._turn_rate)
        elif dir.name == Direction.COUNTERCLOCKWISE:
            self.left_motor.run(-self._turn_rate)
            self.right_motor.run(self._turn_rate)
        else:
            print("ERROR: Illegal Direction!")

    def reset_distance(self):
        self.drive_base.reset()

    def get_distance(self):
        return self.drive_base.distance()

    def spin(self):
        self.drive_base.turn(360)

    def go_distance(self, dist):
        self.reset_distance()
        self.go_forward()
        while self.get_distance() < dist:
            pass
        self.hold()
