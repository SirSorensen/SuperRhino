from pybricks.parameters import Direction

class Angle_Utils:
    def convert_degrees(degrees):
        while degrees < 0:
            degrees += 360
        return (360 - (degrees)) % 360

    def to_movement_degrees(degrees):
        value = degrees % 360
        if value > 180:
            value -= 360
        return value

    def get_direction(degrees):
        degrees = Angle_Utils.to_movement_degrees(degrees)
        if degrees >= 0:
            return Direction.CLOCKWISE
        else:
            return Direction.COUNTERCLOCKWISE