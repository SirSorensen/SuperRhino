
from utils.point import Point
from utils.regression import Linear_Regression, mid_linear_regression


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

        self.left_border_fun = Linear_Regression.from_points(pl1, pl2)
        self.right_border_fun = Linear_Regression.from_points(pr1, pr2)
        self.mid_fun = mid_linear_regression(self.left_border_fun, self.right_border_fun)

        mid_l = pl1.mid_point(pl2)
        mid_r = pr1.mid_point(pr2)
        self.center = mid_l.mid_point(mid_r)




