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


    def start_forward(self):
        self.left_motor.run(self.speed)
        self.right_motor.run(self.speed)

    def start_backward(self):
        self.left_motor.run(-self.speed)
        self.right_motor.run(-self.speed)

    def hold(self):
        self.left_motor.hold()
        self.right_motor.hold()

    def start_turn(self, dir: Direction, turn_rate: int = 0):
        if turn_rate == 0:
            turn_rate = self._turn_rate

        if dir.name == Direction.CLOCKWISE:
            self.left_motor.run(turn_rate)
            self.right_motor.run(-turn_rate)
        elif dir.name == Direction.COUNTERCLOCKWISE:
            self.left_motor.run(-turn_rate)
            self.right_motor.run(turn_rate)
        else:
            print("ERROR: Illegal Direction!")

    def turn_degrees(self, degrees):
        angle = degrees
        self.drive_base.turn(angle)

    def distance(self):
        return self.drive_base.distance()
