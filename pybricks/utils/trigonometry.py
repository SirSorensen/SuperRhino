
# Angle -> degrees counter clockwise
# Degrees -> degrees clockwise

class Trigonometry:
    # d1 = Direction 1
    def calc_diff(degrees1: float, degrees2: float):
        r1 = degrees2 - degrees1
        r2 = degrees2 - degrees1 - 360
        r3 = degrees2 - degrees1 + 360
        return min(r1, r2, r3, key=lambda r: abs(r))