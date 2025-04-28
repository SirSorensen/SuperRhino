
class RobotPose:
    def __init__(self, x: float, y: float, theta: float):
        self.x: float = x
        self.y: float = y
        self.theta: float = theta

    # this is for pretty printing
    def __repr__(self) -> str:
        return f"x:{self.x},y:{self.y},theta:{self.theta}"
