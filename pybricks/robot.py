from pybricks.parameters import Port
from pybricks.hubs import PrimeHub

from mind.spatial_awareness import Spatial_Awareness
from mind.planner import Planner

from senses.vision import Vision
from senses.compass import Compass

from physiology.movement import Movement


class Robot:
    def __init__(self):
        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()

        # Initialise Motors (wheels)
        self.movement: Movement = Movement(Port.B, Port.A)

        # Initialize & calibrate the sensors
        self.vision: Vision = Vision(Port.F, Port.E)
        self.compass: Compass = Compass(self.prime_hub.imu)

    def sokoban(self, solution_str: str, start_coords):
        self.planner: Planner = Planner(solution_str)
        self.consciousness: Spatial_Awareness = Spatial_Awareness(start_coords)

        while not self.planner.is_done():
            next_move = self.planner.next_move()
            print("\nNext move =", next_move)
            turn_degree = self.consciousness.next_angle(next_move)
            print(f"Gotta turn {turn_degree} degrees")
