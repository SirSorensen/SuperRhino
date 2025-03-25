from utils.point import Point
import umath as math


class Regression:
    def linear_regression(point1: Point, point2: Point):
        vx, vy = point1.to_vector(point2)
        slope = vy / vx
        zero_y = point1.Y - (slope * point1.X)

        def fun(x: float) -> float:
            return x * slope + zero_y

        return fun
