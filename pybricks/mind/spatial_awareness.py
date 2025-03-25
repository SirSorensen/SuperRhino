from mind.utils.cardinal_direction import CardinalDirection, diff
from mind.utils.point import Point
from senses.utils.trigonometry import Trigonometry


class Spatial_Awareness:
    def __init__(self, start_position: tuple[float, float] = (0, 0), start_direction: CardinalDirection = CardinalDirection.E):
        self.cur_direction: CardinalDirection = start_direction
        self.cur_position: Point = Point(start_position)

        self.last_dist = 0

    def next_angle(self, next_dir: CardinalDirection) -> float:
        result = diff(self.cur_direction, next_dir)
        self.cur_direction = next_dir
        return result

    def update_pos(self, dist, cur_heading):
        # Calcs
        change_in_dist = dist - self.last_dist
        change_vector = Trigonometry.to_vector(change_in_dist, cur_heading)
        # Update properties
        self.cur_position.update(change_vector)
        self.last_dist = dist
