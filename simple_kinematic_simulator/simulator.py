from environment import Environment
from robot import DifferentialDriveRobot


class Simulator:
    def __init__(self, width, height, i = 0.2, motor_speed = 2, timestep = 0.1, controller=None):
        """
        Simulator for differential drive robot in an environment.
        Args:
            width (float): environment width (cm)
            height (float): environment height (cm)
            i (float): initial proportional gain for baseline controller (unused if controller provided)
            motor_speed (float): default motor speed (rad/s) for baseline controller (unused if controller provided)
            timestep (float): time step (s) per simulation tick
            controller (Controller, optional): custom controller instance to use; if None, a BaselineController is created
        """
        self.env = Environment(width, height)
        # Initialize robot with optional custom controller
        self.robot = DifferentialDriveRobot(
            self.env,
            width/2 - 100,
            height/2 - 100,
            0,
            i,
            motor_speed=motor_speed,
            controller=controller
        )
        self.timestep = timestep
    
    # simulate one execution cycle of the robot
    def run_tick(self):
        robot_pose = self.robot.move(self.timestep)
        print(f"Current position = {robot_pose}")

