from mind.utils.cardinal_direction import CardinalDirection, diff
from mind.utils.point import Point
from mind.utils.trigonometry import Trigonometry


class Spatial_Awareness:
    def __init__(self, dist_to_eye: tuple[float, float], start_position: tuple[float, float] = (0, 0), start_direction: CardinalDirection = CardinalDirection.E):
        self.cur_direction: CardinalDirection = start_direction
        self.cur_position: Point = Point(start_position)


        eye_x, eye_y = dist_to_eye
        self.dist_eye_right = Point((abs(eye_x), eye_y))
        self.dist_eye_left = Point((-abs(eye_x), eye_y))

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

    def get_eyes_posses(self) -> tuple[Point, Point]:
        left = self.cur_position.sum(self.dist_eye_left)
        right = self.cur_position.sum(self.dist_eye_right)
        return (left, right)
