from utils.cardinal_direction import CardinalDirection, to_angle
from utils.trigonometry import Trigonometry


class Spatial_Awareness:
    def __init__(self, x, y):
        self.pos = (x, y)

    def next_angle(self, next_dir: CardinalDirection) -> float:
        cur_angle = to_angle(self.cur_direction)
        next_angle = to_angle(next_dir)
        result = Trigonometry.calc_diff(cur_angle, next_angle)
        self.cur_direction = next_dir
        return result


    def get_next_pos(self, v):
        dx, dy = v
        x, y = self.pos
        return (x + dx, y + dy)

    def set_next_pos(self, v):
        self.pos = self.get_next_pos(v)