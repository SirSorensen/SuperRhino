

class Angle:
    def __init__(self, degree):
        self.value = degree % 360
        if self.value > 180:
            self.value -= 360

    def to_angle(degree) -> float:
        angle = Angle(degree)
        return angle.value



