class Point(object):
    def __init__(self, vals : tuple[float, float]):
        self.X, self.Y = vals

    def update(self, vector):
        (dx, dy) = vector
        self.X = self.X + dx
        self.Y = self.Y + dy

    def __add__(self, other):
        return Point((self.X + other.X, self.Y + other.Y))

    def __sub__(self, other):
        return Point((self.X - other.X, self.Y - other.Y))