
class State:
    """State which the robot can be in"""
    ON_INTERSECTION: int = 1
    BETWEEN_POINTS: int = 2
    OFF_GRID: int = 3

class VisionObject:
    """Objects the robot can see"""
    TABLE   : str = "TABLE"
    TAPE    : str = "TAPE"
    EDGE    : str = "EDGE"
    UNKNOWN : str = "UNKNOWN"

