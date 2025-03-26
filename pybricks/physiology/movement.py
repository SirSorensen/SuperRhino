from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from utils.angle_utils import Angle_Utils


class Movement:
    def __init__(
                 self, left_motor_port: Port, right_motor_port: Port,
                 wheel_diameter=56, axle_track=85,
                 _turn_rate=100, _turn_degree=40, _speed=400
                ):
        # Initialise Motors (wheels)
        self.left_motor: Motor = Motor(left_motor_port, Direction.COUNTERCLOCKWISE)
        self.right_motor: Motor = Motor(right_motor_port)

        self.drive_base: DriveBase = DriveBase(self.left_motor, self.right_motor, wheel_diameter=wheel_diameter, axle_track=axle_track)

        self.turn_rate = _turn_rate
        self.turn_degree = _turn_degree
        self.speed = _speed


    def start_forward(self, magnitude = 1):
        self.left_motor.run(self.speed * magnitude)
        self.right_motor.run(self.speed * magnitude)

    def hold(self):
        self.left_motor.hold()
        self.right_motor.hold()

    def start_turn(self, dir: Direction, magnitude = 1):

        if dir == Direction.CLOCKWISE:
            self.left_motor.run(self.turn_rate * magnitude)
            self.right_motor.run(-self.turn_rate * magnitude)
        elif dir == Direction.COUNTERCLOCKWISE:
            self.left_motor.run(-self.turn_rate * magnitude)
            self.right_motor.run(self.turn_rate * magnitude)
        else:
            print("ERROR: Illegal Direction!")

    def turn_degrees(self, degrees):
        if degrees == 0:
            return
        movement_degrees = Angle_Utils.to_movement_degrees(degrees)
        print(f"Turning {movement_degrees} degrees!")
        self.drive_base.turn(movement_degrees)

    def distance(self):
        """
            Gets the estimated driven distance.

            Returns:
                Driven distance since last reset (in mm).
        """
        return self.drive_base.distance()

