class Point(object):
    def __init__(self, vals : tuple[float, float]):
        self.X, self.Y = vals

    def update(self, vector):
        (dx, dy) = vector
        self.X = self.X + dx
        self.Y = self.Y + dy

    def to_vector(self, other) -> tuple[float, float]:
        if type(other) is not Point:
            raise KeyError("other has to be a Point")
        return (other.X - self.X, other.Y - self.Y)

    def sum(self, other):
        if type(other) is not Point:
            raise KeyError("other has to be a Point")
        return Point(other.X + self.X, other.Y + self.Y)

    def __str__(self):
        return f"({self.X}, {self.Y})"