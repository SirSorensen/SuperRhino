from Simulator.environment import Environment
from Robot.robot import DifferentialDriveRobot
from Simulator.sim_state import SimulatorState


class Simulator:
    def __init__(self, width, height, i=0.2, motor_speed=2, timestep=0.1):
        self.env = Environment(width, height)
        self.robot = DifferentialDriveRobot(self.env, width / 2 - 100, height / 2 - 100, 0, i, motor_speed=motor_speed)
        self.timestep = timestep

    # simulate one execution cycle of the robot
    def run_tick(self):
        self.robot.move(self.timestep)

    def get_state(self) -> SimulatorState:
        return SimulatorState(self.robot, self.env, self.timestep)

    def gen_from_state(sim_state: SimulatorState):
        return Simulator(sim_state.env_width, sim_state.env_height, i=sim_state.robot_i, motor_speed=sim_state.robot_motor_speed, timestep=sim_state.timestep)
