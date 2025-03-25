from pybricks.parameters import Direction
import umath as math

class Trigonometry:
    def to_vector(dist, angle):
        radians = math.radians(angle)
        x = dist*math.cos(radians)
        y = dist*math.sin(radians)
        return (x,y)

    # d1 = Direction 1
    def calc_diff(d1 : float, d2 : float):
        r1 = d2 - d1
        r2 = d2 - d1 - 360
        r3 = d2 - d1 + 360
        return min(r1, r2, r3, key=lambda r: abs(r))


    def calc_angle(vector):
        # cos(a) = abs(x) / sqrt(x^2+y^2)
        vx, vy = vector
        v_length = math.sqrt(math.pow(vx, 2) + math.pow(vy, 2))
        x_length = abs(vx)
        abs_radians = math.acos(x_length / v_length)
        abs_degrees = math.degrees(abs_radians)

        if vx < 0 and vy < 0:
            abs_degrees += 180
        elif vx < 0:
            abs_degrees += 90
        elif vy < 0:
            abs_degrees += 270

        return abs_degrees

    def get_direction(degrees):
        if degrees >= 0:
            return Direction.CLOCKWISE
        else:
            return Direction.COUNTERCLOCKWISE
