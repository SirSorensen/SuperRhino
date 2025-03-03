import calibrations as cal
from enums import SimpleDirection

from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import ColorSensor, Motor


class Robot:
    def __init__(self):
        # Initialise Motors (wheels)
        self.left_motor: Motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.right_motor: Motor = Motor(Port.E)

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)

        # Initialize & calibrate the sensors.
        self.left_sensor: ColorSensor = ColorSensor(Port.B)
        self.left_threshold = cal.calibrate_light_sensor(self, self.left_sensor)

        self.right_sensor: ColorSensor = ColorSensor(Port.F)
        self.right_threshold = cal.calibrate_light_sensor(self, self.right_sensor)

        # Calibrate acceleration:
        self.acceleration_error = cal.calibrate_acceleration(self)

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