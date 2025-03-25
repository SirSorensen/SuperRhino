from utils.trigonometry import Trigonometry
from utils.point import Point
import umath as math

class Linear_Regression:
    def __init__(self, slope, zero_y):
        self.slope = slope
        self.zero_y = zero_y
        self.angle = Trigonometry.calc_angle(1, self.slope)


    def fun(self, x):
        return x * self.slope + self.zero_y


    def from_points(point1: Point, point2: Point):
        vx, vy = point1.to_vector(point2)
        slope = vy / vx
        zero_y = point1.Y - (slope * point1.X)
        return Linear_Regression(slope, zero_y)


    def dist(self, point: Point):
        return abs(self.slope*point.X - 1 * point.Y + self.zero_y) / math.sqrt(math.pow(self.slope, 2) + math.pow(self.zero_y, 2))


    def closest_point(self, source_point: Point):
        x0 = source_point.X
        y0 = source_point.Y
        a = self.slope
        b = -1
        c = self.zero_y

        x = x0 - ((a*x0 + b*y0 + c) / (a**2 + b**2))
        y = y0 + ((a*x0 + b*y0 + c) / (a**2 + b**2))

        return Point((x, y))



def mid_linear_regression(left : Linear_Regression, right : Linear_Regression):
    avg_slope = (left.slope + right.slope) / 2
    avg_zero = (left.zero_y + right.zero_y) / 2
    return Linear_Regression(avg_slope, avg_zero)
