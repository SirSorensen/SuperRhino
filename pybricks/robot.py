from pybricks.parameters import Port
from pybricks.hubs import PrimeHub
import robot_helper as helper
from awareness.planner import Planner
from awareness.consciousness import Consciousness
from senses.vision import Vision
from senses.compass import Compass
from communication.vocals import Vocals
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

        # Initialize speakers and back-lights
        self.vocals: Vocals = Vocals(self.prime_hub.speaker)

        # Calibrations
        self.calibrate_compass()

    def sokoban(self, solution_str: str, rhinotron_coords, rhinotron_compass="E"):
        self.planner: Planner = Planner(solution_str)
        self.consciousness: Consciousness = Consciousness(rhinotron_compass, rhinotron_coords)

        while not self.planner.is_done():
            next_move = self.planner.next_move()
            print("\nNext move =", next_move)
            turn_degree, move_dist = self.consciousness.next(next_move)
            self.vocals.boop_beep()
            self.movement, self.compass = helper.go(self.movement, self.compass, turn_degree, move_dist)
            self.vocals.beep_boop()

        self.prime_hub.speaker.play_notes(["C4/4", "C4/4", "G4/4", "G4/4"])

    ########################## Calibrations: ##########################

    def calibrate_compass(self):
        ###  0  ###
        self.compass.add_heading_error(0)
        ### -30 ###
        self.movement.turn(-30)
        self.compass.add_heading_error(-30)
        ### -60 ###
        self.movement.turn(-30)
        self.compass.add_heading_error(-60)
        ### -90 ###
        self.movement.turn(-30)
        self.compass.add_heading_error(-90)
        ###  0 ###
        self.movement.turn(90)
        self.compass.add_heading_error(0)
        ###  30 ###
        self.movement.turn(30)
        self.compass.add_heading_error(30)
        ###  60 ###
        self.movement.turn(30)
        self.compass.add_heading_error(60)
        ###  90 ###
        self.movement.turn(30)
        self.compass.add_heading_error(90)
        ###  0  ###
        self.movement.turn(-90)
        self.compass.add_heading_error(0)

        ### Done ###
        self.compass.finish_calibrate_heading()
