from utils.point import Point
from utils.trigonometry import Trigonometry
from utils.vector import Vector


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

        self.left_border_angle = pl1.to_vector(pl2).degrees()
        print(f"Left tape angle: {self.left_border_angle}")
        self.right_border_angle = pr1.to_vector(pr2).degrees()
        print(f"Right tape angle: {self.right_border_angle}")
        self.mid_angle = Trigonometry.calc_mid(self.left_border_angle, self.right_border_angle)
        print(f"Mid tape angle: \n{self.mid_angle}", end="\n\n")

        mid_l = pl1.mid_point(pl2)
        mid_r = pr1.mid_point(pr2)
        self.center = mid_l.mid_point(mid_r)
        self.front_center = pl2.mid_point(pr2)

    def diff(self, cur_position: Point):
        distance = self.center.dist(cur_position)
        expected_vector = Vector.from_dist_degrees(distance, self.mid_angle)
        actual_vector = self.center.to_vector(cur_position)
        error_degrees = expected_vector.degrees_to(actual_vector)
        return Trigonometry.calc_side_dist(distance, error_degrees)
