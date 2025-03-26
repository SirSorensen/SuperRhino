import umath as math
from utils.angle_utils import Angle_Utils

class Vector(object):
    def __init__(self, x, y):
        self.X, self.Y = x, y

    def from_dist_degrees(magnitude, degrees):
        angle = Angle_Utils.convert_degrees(degrees)
        radians = math.radians(angle)
        x = magnitude * math.cos(radians)
        y = magnitude * math.sin(radians)
        return Vector(x, y)

    def length(self):
        return math.sqrt(self.X**2 + self.Y**2)

    def rotate(self, degrees):
        angle = Angle_Utils.convert_degrees(degrees)
        radians = math.radians(angle)
        trans_x = math.cos(radians) * self.X + math.sin(radians) * self.Y
        trans_y = math.sin(radians) * self.X - math.cos(radians) * self.Y
        return (trans_x, trans_y)

    def degrees_to(self, other):
        # angle = cos^-1((v1 dot v2) / (length of v1 * length of v2))
        dot_product = self.X * other.X + self.Y * other.Y
        radians = math.acos(dot_product / (self.length() * other.length()))
        angle = math.degrees(radians)
        return Angle_Utils.convert_degrees(angle)