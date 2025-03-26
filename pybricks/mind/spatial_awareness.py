from utils.cardinal_direction import CardinalDirection, to_angle
from utils.point import Point
from utils.trigonometry import Trigonometry


class Spatial_Awareness:
    def __init__(self, dist_to_eye: tuple[float, float], start_position: tuple[float, float] = (0, 0), start_direction: CardinalDirection = CardinalDirection.E):
        self.cur_direction: CardinalDirection = start_direction
        self.cur_position: Point = Point(start_position)

        eye_x, eye_y = dist_to_eye

        self.right_eye_vector = (eye_x, -eye_y)
        self.left_eye_vector = (eye_x, eye_y)

        self.last_dist = 0

    def next_angle(self, next_dir: CardinalDirection) -> float:
        cur_angle = to_angle(self.cur_direction)
        next_angle = to_angle(next_dir)
        result = Trigonometry.calc_diff(cur_angle, next_angle)
        self.cur_direction = next_dir
        return result

    def update(self, dist, cur_heading):
        # Calcs
        change_in_dist = dist - self.last_dist
        change_vector = Trigonometry.to_vector(change_in_dist, cur_heading)
        # Update properties
        self.cur_position = self.cur_position.add_vector(change_vector)
        self.last_dist = dist

    def get_eyes_posses(self, cur_heading) -> tuple[Point, Point]:
        trans_left = Trigonometry.transform_vector(self.left_eye_vector, cur_heading)
        trans_right = Trigonometry.transform_vector(self.right_eye_vector, cur_heading)
        left = self.cur_position.add_vector(trans_left)
        right = self.cur_position.add_vector(trans_right)
        return (left, right)

    def print_status(self):
        print()
        print(f"Current position      = {self.cur_position}")
        print(f"Current direction     = {self.cur_direction}")
        print(f"Current eye positions = {self.get_eyes_posses()}")
        print()
