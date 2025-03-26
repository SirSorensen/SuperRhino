from utils.vector import Vector

class Point(object):
    def __init__(self, x : float, y : float):
        self.X, self.Y = x, y

    def from_tuple(vals : tuple[float, float]):
        x, y = vals
        return Point(x, y)

    def add_vector(self, vector : Vector):
        x = self.X + vector.X
        y = self.Y + vector.Y
        return Point(x, y)

    def to_vector(self, other) -> Vector:
        if type(other) is not Point:
            raise KeyError("other has to be a Point")
        return Vector(other.X - self.X, other.Y - self.Y)

    def dist(self, other):
        if type(other) is not Point:
            raise KeyError("other has to be a Point")
        return self.to_vector(other).length()

    def __str__(self):
        return f"({self.X}, {self.Y})"

    def mid_point(self, other):
        if type(other) is not Point:
            raise KeyError("other has to be a Point")

        v = self.to_vector(other)
        return Point(self.X + (v.X/2), self.Y + (v.Y/2))