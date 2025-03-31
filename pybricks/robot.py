from mind.planner import Planner
from mind.spatial_awareness import Spatial_Awareness
from physiology.movement import Movement
from utils.cardinal_direction import CardinalDirection
from utils.measurements import Measurements

from pybricks.hubs import PrimeHub
from pybricks.parameters import Port

print_method_calls = True


class Robot:
    def __init__(self):
        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()

        # Initialise Motors (wheels)
        self.movement: Movement = Movement(Port.B, Port.A)

        self.measurements = Measurements()

    ########################## sokoban ##########################

    def sokoban(self, solution_str: str):
        self.planner: Planner = Planner(solution_str)
        self.spatial_awareness: Spatial_Awareness = Spatial_Awareness(0, 3)
        self.movement.drive_base.reset()
        self.movement.drive_base.use_gyro(True)


        while not self.planner.is_done():
            next_move = self.planner.next_move()

            if next_move == CardinalDirection.CAN:
                next_move = self.planner.next_move()
                next_pos = self.spatial_awareness.get_next_pos(next_move)
                dist = self.measurements.get_push_dist(self.spatial_awareness.pos, next_pos)
                self.do_move(next_move, dist)

                next_pos = self.spatial_awareness.get_next_pos(next_move)
                dist = self.measurements.get_dist(self.spatial_awareness.pos, next_pos)
                self.do_move(next_move, dist)
                next_move = CardinalDirection.get_opposite(next_move)
                self.do_move(next_move, -dist)


            else:
                next_pos = self.spatial_awareness.get_next_pos(next_move)
                dist = self.measurements.get_dist(self.spatial_awareness.pos, next_pos)
                self.do_move(next_move, dist)

            print(f"\n\n\n ################ NEW MOVE ({next_move}) ################")
            print("\nNext move =", next_move, end="\n\n")




    def do_move(self, next_move, dist):
        # Turn correct way
        if dist > 0:
            turn_degrees = self.spatial_awareness.next_angle(next_move)
            self.movement.drive_base.turn(turn_degrees)

        # Go forward
        self.movement.drive_base.straight(dist)
        self.spatial_awareness.set_next_pos(next_move)

