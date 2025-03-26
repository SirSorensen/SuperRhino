from pybricks.parameters import Direction
from utils.point import Point
import umath as math


# Angle -> degrees counter clockwise
# Degrees -> degrees clockwise


class Trigonometry:
    def to_vector(dist, degrees):
        angle = Angle_Utils.convert_degrees(degrees)
        radians = math.radians(angle)
        x = dist * math.cos(radians)
        y = dist * math.sin(radians)
        return (x, y)

    # d1 = Direction 1
    def calc_diff(degrees1: float, degrees2: float):
        r1 = degrees2 - degrees1
        r2 = degrees2 - degrees1 - 360
        r3 = degrees2 - degrees1 + 360
        return min(r1, r2, r3, key=lambda r: abs(r))

    def calc_mid(degrees1: float, degrees2: float):
        diff = Trigonometry.calc_diff(degrees1, degrees2)
        return (max(degrees1, degrees2) - (diff / 2)) % 360

    def calc_angle(vector):
        # cos(a) = abs(x) / sqrt(x^2+y^2)
        vx, vy = vector
        v_length = math.sqrt(math.pow(vx, 2) + math.pow(vy, 2))
        x_length = abs(vx)
        abs_radians = math.acos(x_length / v_length)
        abs_angle = math.degrees(abs_radians)

        if vx < 0 and vy < 0:
            abs_angle += 180
        elif vx < 0:
            abs_angle += 90
        elif vy < 0:
            abs_angle += 270

        return Angle_Utils.convert_degrees(abs_angle)

    def degrees_from_points(point1: Point, point2: Point):
        vx, vy = point1.to_vector(point2)

        radians = math.atan2(vy, vx)
        angle = math.degrees(radians)

        print(f"degrees_from_points -> {angle} => {Angle_Utils.convert_degrees(angle)}")

        return Angle_Utils.convert_degrees(angle)

    def transform_vector(vector, degrees):
        x, y = vector
        angle = Angle_Utils.convert_degrees(degrees)
        radians = math.radians(angle)
        trans_x = math.cos(radians) * x + math.sin(radians) * y
        trans_y = math.sin(radians) * x - math.cos(radians) * y
        return (trans_x, trans_y)

    def get_direction(degrees):
        if degrees >= 0:
            return Direction.CLOCKWISE
        else:
            return Direction.COUNTERCLOCKWISE

    def length_of_vector(vector):
        return math.sqrt(sum([v**2 for v in vector]))

    def degrees_between_vectors(v1, v2):
        v1x, v1y = v1
        v2x, v2y = v2
        # angle = cos^-1((v1 dot v2) / (length of v1 * length of v2))
        dot_product = v1x * v2x + v1y * v2y
        v1_length = Trigonometry.length_of_vector(v1)
        v2_length = Trigonometry.length_of_vector(v2)
        radians = math.acos(dot_product / (v1_length * v2_length))
        angle = math.degrees(radians)
        return Angle_Utils.convert_degrees(angle)

    def calc_terminal_point(distance, degrees): # Terminal point = point of intersection on a unit circle
        angle = Angle_Utils.convert_degrees(degrees)
        x = math.cos(angle)
        y = math.sin(angle)
        return Point((x, y))

    def calc_side_dist(magnitude, degrees_between_vectors): # How far are we off course
        angle = Angle_Utils.convert_degrees(degrees_between_vectors)
        unit_distance = -math.sin(angle)
        return unit_distance * magnitude




class Angle_Utils:
    def convert_degrees(degrees):
        while degrees < 0:
            degrees += 360
        return (360 - (degrees)) % 360

    def to_movement_degrees(degrees):
        value = degrees % 360
        if value > 180:
            value -= 360
        return value
