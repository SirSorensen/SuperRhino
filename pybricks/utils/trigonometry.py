import umath as math

class Trigonometry:
    def to_vector(dist, angle):
        radians = math.radians(angle)
        x = dist*math.cos(radians)
        y = dist*math.sin(radians)
        return (x,y)

    def calc_diff(d1 : float, d2 : float):
        r1 = d2 - d1
        r2 = d2 - d1 - 360
        r3 = d2 - d1 + 360
        return min(r1, r2, r3, key=lambda r: abs(r))