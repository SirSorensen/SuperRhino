
from Robot.robot import DifferentialDriveRobot
from Robot.robot_pose import RobotPose
from Simulator.environment import Environment

class SimulatorState:
    def __init__(self, robot : DifferentialDriveRobot, env : Environment, timestep):
        self.robot_position : RobotPose = robot.get_robot_pose()
        self.robot_mid_dist = robot.get_mid_distance()
        self.robot_i = robot.i
        self.robot_motor_speed = robot.motor_speed
        self.robot_radius = robot.get_robot_radius()
        (self.robot_left_speed, self.robot_right_speed) = robot.get_robot_speed()
        self.env_width = env.width
        self.env_height = env.height
        self.timestep = timestep


    def print(self):
        print(f"Robot i = {self.robot_i}")
        print(f"Robot final position = {self.robot_position}")
        print(f"Robot final distance to wall = {self.robot_mid_dist}")

    def print_coefficients(self):
        print(f"Robot's i = {self.robot_i} ; Motor speed = {self.robot_motor_speed}")

    def print_result(self):
        print(f"Distance from mid to wall = {self.robot_mid_dist + self.robot_radius} ; Final speed = {(self.robot_left_speed + self.robot_right_speed) / 2}")
