
class Orientation:
    """Robot orientation in a 2D-space"""
    N: tuple[int, int] = ( 0,  1)
    S: tuple[int, int] = ( 0, -1)
    W: tuple[int, int] = (-1,  0)
    E: tuple[int, int] = ( 1,  0)

class State:
    """State which the robot can be in"""
    ON_INTERSECTION: int = 1
    BETWEEN_POINTS: int = 2
    OFF_GRID: int = 3