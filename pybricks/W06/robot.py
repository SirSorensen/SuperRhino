from enums import SimpleDirection


class Robot:
    def __init__(self):
        pass  # TODO

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