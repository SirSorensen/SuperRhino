from physiology.movement import Movement
from pybricks.parameters import Port
from pybricks.hubs import PrimeHub
from mind.planner import Planner
from mind.consciousness import Consciousness


class Robot:
    def __init__(self):

        # Initialise Motors (wheels)
        self.movement: Movement = Movement(Port.B, Port.A)

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(10)


    def sokoban_prep(self, solution_str : str, rhinotron_coords):
        self.planner : Planner = Planner(solution_str)
        self.consciousness : Consciousness = Consciousness("E", rhinotron_coords)

    def sokoban_run(self):
        while not self.planner.is_done():
            next_move = self.planner.next_move()
            print("\nNext move =", next_move)
            turn_degree, move_dist = self.consciousness.next(next_move)
            self.movement.turn(turn_degree)
            self.prime_hub.speaker.beep(120, 50)
            self.prime_hub.speaker.beep(140, 50)
            self.movement.go_distance(move_dist*10)
            self.prime_hub.speaker.beep(150, 50)
            self.prime_hub.speaker.beep(130, 50)

        self.prime_hub.speaker.play_notes(['C4/4', 'C4/4', 'G4/4', 'G4/4'])