from pybricks.parameters import Port
from pybricks.hubs import PrimeHub
from mind.planner import Planner
from mind.consciousness import Consciousness
from senses.vision import Vision
from senses.directional import Sense_of_Direction
from communication.vocals import Vocals
from physiology.movement import Movement


class Robot:
    def __init__(self):
        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()

        # Initialise Motors (wheels)
        self.movement: Movement = Movement(Port.B, Port.A)

        # Initialize & calibrate the sensors
        self.vision : Vision = Vision(Port.F, Port.E)
        self.direction : Sense_of_Direction = Sense_of_Direction(self.prime_hub.imu)

        # Initialize speakers and back-lights
        self.vocals : Vocals = Vocals(self.prime_hub.speaker)

        # Calibrations
        self.calibrate_direction()


    def sokoban_prep(self, solution_str : str, rhinotron_coords):
        self.planner : Planner = Planner(solution_str)
        self.consciousness : Consciousness = Consciousness("E", rhinotron_coords)

    def sokoban_run(self):
        while not self.planner.is_done():
            next_move = self.planner.next_move()
            print("\nNext move =", next_move)
            turn_degree, move_dist = self.consciousness.next(next_move)
            self.movement.turn(turn_degree)
            self.vocals.boop_beep()
            self.prime_hub.speaker.beep(140, 50)
            self.movement.go_distance(move_dist*10)
            self.vocals.beep_boop()

        self.prime_hub.speaker.play_notes(['C4/4', 'C4/4', 'G4/4', 'G4/4'])


    ########################## Calibrations: ##########################

    def calibrate_direction(self):
        ###  0  ###
        self.direction.add_heading_error(0)
        ### -30 ###
        self.movement.turn(-30)
        self.direction.add_heading_error(-30)
        ### -60 ###
        self.movement.turn(-30)
        self.direction.add_heading_error(-60)
        ### -90 ###
        self.movement.turn(-30)
        self.direction.add_heading_error(-90)
        ###  0 ###
        self.movement.turn(90)
        self.direction.add_heading_error(0)
        ###  30 ###
        self.movement.turn(30)
        self.direction.add_heading_error(30)
        ###  60 ###
        self.movement.turn(30)
        self.direction.add_heading_error(60)
        ###  90 ###
        self.movement.turn(30)
        self.direction.add_heading_error(90)
        ###  0  ###
        self.movement.turn(-90)
        self.direction.add_heading_error(0)

        ### Done ###
        self.direction.finish_calibrate_heading()