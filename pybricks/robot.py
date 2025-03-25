from pybricks.parameters import Port
from pybricks.hubs import PrimeHub

from mind.spatial_awareness import Spatial_Awareness
from mind.planner import Planner

from utils.state import VisionObject
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

        # Initialize & awareness
        self.spatial_awareness: Spatial_Awareness = Spatial_Awareness((2,4)) #TODO: Measure dist to eyes

        # Calibrations
        self.calibrate_compass()

    def sokoban(self, solution_str: str):
        self.planner: Planner = Planner(solution_str)

        while not self.planner.is_done():
            next_move = self.planner.next_move()
            print("\nNext move =", next_move)

            # Turn correct way
            turn_degrees = self.spatial_awareness.next_angle(next_move)
            print(f"Gotta turn {turn_degrees} degrees")
            self.movement.turn_degrees(turn_degrees)

            # Go forward
            self.goto_next_intersection()


    def goto_next_intersection(self):
        correct_angle = self.compass.direction()

        while True:
            self.movement.start_forward()

            self.spatial_awareness.update(self.movement.distance(), self.compass.direction())
            self.spatial_awareness.print_status()

            if self.compass.angle_needs_correcting(correct_angle):
                self.movement.hold()
                angle_error = self.compass.calc_error(correct_angle)
                self.movement.turn_degrees(angle_error)
                self.movement.start_forward()

            # I see not table!
            if self.vision.what_is_seen() != (VisionObject.TABLE, VisionObject.TABLE):
                self.movement.hold()

                # If it is NOT an intersection, then it is probably due to being hit
                if not self.detect_intersection():
                    self.fix_angle()

                # If it is an intersection, then keep going until in the middle of intersection
                else:
                    pass


    def detect_intersection(self) -> bool:
        pass


    def fix_angle(self):
        pass


    ########################## Calibrations: ##########################

    def calibrate_compass(self):
        ###  0  ###
        self.compass.add_heading_error(0)
        ### -30 ###
        self.movement.turn_degrees(-30)
        self.compass.add_heading_error(-30)
        ### -60 ###
        self.movement.turn_degrees(-30)
        self.compass.add_heading_error(-60)
        ### -90 ###
        self.movement.turn_degrees(-30)
        self.compass.add_heading_error(-90)
        ###  0 ###
        self.movement.turn_degrees(90)
        self.compass.add_heading_error(0)
        ###  30 ###
        self.movement.turn_degrees(30)
        self.compass.add_heading_error(30)
        ###  60 ###
        self.movement.turn_degrees(30)
        self.compass.add_heading_error(60)
        ###  90 ###
        self.movement.turn_degrees(30)
        self.compass.add_heading_error(90)
        ###  0  ###
        self.movement.turn_degrees(-90)
        self.compass.add_heading_error(0)

        ### Done ###
        self.compass.finish_calibrate_heading()
