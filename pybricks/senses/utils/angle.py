import umath as math

class Angle:
    def __init__(self, degree):
        self.value = degree

    def to_angle(degree) -> float:
        value = degree % 360
        if value > 180:
            value -= 360
        return value

    def to_angle_from_radians(radians) -> float:
        degrees = math.degrees(radians)
        return degrees

    def calc_diff(d1 : float, d2 : float):
        r1 = d2 - d1
        r2 = d2 - d1 - 360
        r3 = d2 - d1 + 360
        return min(r1, r2, r3, key=lambda r: abs(r))


if __name__ == "__main__":
    print(Angle.calc_diff(357, 3))