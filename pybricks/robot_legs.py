from enums import SimpleDirection

from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor


class RobotLegs:
    def __init__(self, left_port : Port, right_port : Port):
        # Initialise Motors (wheels)
        self.left_motor: Motor = Motor(left_port, Direction.COUNTERCLOCKWISE)
        self.right_motor: Motor = Motor(right_port)

    def go_forward(self):
        pass  # TODO

    def go_back(self):
        pass  # TODO

    def turn(self, angle):
        pass  # TODO

    def turn_direction(self, direction: SimpleDirection):
        match direction:
            case SimpleDirection.FORWARD:
                pass  # TODO
            case SimpleDirection.BACK:
                pass  # TODO
            case SimpleDirection.LEFT:
                pass  # TODO
            case SimpleDirection.RIGHT:
                pass  # TODO
            case _:
                raise ValueError(f"Robot cannot turn in given direction: '{direction}'")