from environment import Environment
from robot import DifferentialDriveRobot


class Simulator:
    def __init__(self, width, height, i = 0.2, motor_speed = 2, timestep = 0.1):
        self.env = Environment(width, height)
        self.robot = DifferentialDriveRobot(self.env, width/2-100, height/2-100, 0, i, motor_speed=motor_speed)
        self.timestep = timestep
    
    # simulate one execution cycle of the robot
    def run_tick(self):
        robot_pose = self.robot.move(self.timestep)
        print(f"Current position = {robot_pose}")

