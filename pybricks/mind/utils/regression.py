
from mind.utils.point import Point
import umath as math

class Regression:
    def calc_angle(point1 : Point, point2 : Point):
        # cos(a) = abs(x) / sqrt(x^2+y^2)
        vx, vy = point1.to_vector(point2)
        v_length = math.sqrt(math.pow(vx, 2) + math.pow(vy, 2))
        x_length = abs(vx)
        abs_radians = math.acos(x_length/v_length)
        abs_degrees = math.degrees(abs_radians)

        if vx < 0 and vy < 0:
            abs_degrees += 180
        elif vx < 0:
            abs_degrees += 90
        elif vy < 0:
            abs_degrees += 270

        return abs_degrees

    def linear_regression(point1 : Point, point2 : Point):
        vx, vy = point1.to_vector(point2)
        slope = vy/vx
        zero_y = point1.Y - (slope * point1.X)

        def fun(x : float) -> float:
            return x * slope + zero_y

        return fun




