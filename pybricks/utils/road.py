from utils.point import Point
from utils.trigonometry import Trigonometry


class Road:
    def __init__(self, pl1: Point, pl2: Point, pr1: Point, pr2: Point):
        """
            Initialize a road

            Arguments:
            pl1 : Left+back point
            pl2 : Left+front point
            pr1 : Right+back point
            pr2 : Right+front point
        """

        self.left_border_angle = Trigonometry.degrees_from_points(pl1, pl2)
        print(f"Left tape angle: {self.left_border_angle}")
        self.right_border_angle = Trigonometry.degrees_from_points(pr1, pr2)
        print(f"Right tape angle: {self.right_border_angle}")
        self.mid_angle = Trigonometry.calc_mid(self.left_border_angle, self.right_border_angle)
        print(f"Mid tape angle: \n{self.mid_angle}", end="\n\n")

        mid_l = pl1.mid_point(pl2)
        mid_r = pr1.mid_point(pr2)
        self.center = mid_l.mid_point(mid_r)

    def diff(self, cur_position: Point):
        distance = self.center.dist(cur_position)
        expected_vector = Trigonometry.to_vector(distance, self.mid_angle)
        actual_vector = self.center.to_vector(cur_position)
        error_degrees = Trigonometry.degrees_between_vectors(expected_vector, actual_vector)
        return Trigonometry.calc_side_dist(distance, error_degrees)
