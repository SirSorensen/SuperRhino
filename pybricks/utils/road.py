from utils.point import Point
from utils.trigonometry import Trigonometry


class Road:
    def __init__(self, pl1: Point, pl2: Point, pl3: Point, pr1: Point, pr2: Point, pr3: Point):
        """
            Initialize a road

            Arguments:
            pl1 : Left+back point
            pl2 : Left+front point
            pr1 : Right+back point
            pr2 : Right+front point
        """

        self.left_border_angle = (pl1.to_vector(pl2).degrees() + pl1.to_vector(pl3).degrees() + pl2.to_vector(pl3).degrees()) / 3
        print(f"Left tape angle: {self.left_border_angle}")
        self.right_border_angle = (pr1.to_vector(pr2).degrees() + pr1.to_vector(pr3).degrees() + pr2.to_vector(pr3).degrees()) / 3
        print(f"Right tape angle: {self.right_border_angle}")
        self.mid_angle = Trigonometry.calc_mid(self.left_border_angle, self.right_border_angle)
        print(f"Mid tape angle: \n{self.mid_angle}", end="\n\n")

        self.front_center = pl3.mid_point(pr3)
