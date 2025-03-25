from mind.utils.orientation import Orientation
from mind.utils.point import Point


class Spatial_Awareness:
    def __init__(self, start_position : tuple[float, float] = (0,0), start_direction : Orientation = Orientation.E):
        self.cur_direction : Orientation = start_direction
        self.cur_position : Point = Point(start_position)
        print("Starting values:")
        print(self.cur_direction)
        print(self.cur_position)

    def cur_angle(self):
        return self.cur_direction

    def update_state(self):
        #TODO: FIGURE OUT STATE / DIRECTION
        pass

    def update_space(self):
        #TODO: FIGURE OUT SPACE
        pass

    def next_angle(self, move : Orientation) -> float:
        # TODO: Take move and return next direction
        result: tuple[float, float] = 0

        print("Next values:")
        print("Direction =", self.cur_direction)
        return result
