import umath as math

class Point(object):
    def __init__(self, x : float, y : float):
        self.X, self.Y = x, y

    def from_tuple(vals : tuple[float, float]):
        x, y = vals
        return Point(x, y)

    def add_vector(self, vector):
        (dx, dy) = vector
        x = self.X + dx
        y = self.Y + dy
        return Point(x, y)

    def to_vector(self, other) -> tuple[float, float]:
        if type(other) is not Point:
            raise KeyError("other has to be a Point")
        return (other.X - self.X, other.Y - self.Y)

    def dist(self, other):
        if type(other) is not Point:
            raise KeyError("other has to be a Point")
        vx, vy = self.to_vector(other)
        return math.sqrt(vx**2 + vy**2)


    def __str__(self):
        return f"({self.X}, {self.Y})"

    def mid_point(self, other):
        if type(other) is not Point:
            raise KeyError("other has to be a Point")

        vx, vy = self.to_vector(other)

        return Point(self.X + (vx/2), self.Y + (vy/2))