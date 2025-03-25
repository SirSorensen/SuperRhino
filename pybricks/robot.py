from pybricks.parameters import Direction
from pybricks.parameters import Port
from pybricks.hubs import PrimeHub

from mind.spatial_awareness import Spatial_Awareness
from mind.planner import Planner

from utils.road import Road
from utils.trigonometry import Trigonometry
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

    def follow_tape(self):
        start_angle = self.compass.direction()

        def slow_and_measure(side : str):
            if side.upper() == "L":
                dir = Direction.COUNTERCLOCKWISE
                eye_index = 0
            else:
                dir = Direction.CLOCKWISE
                eye_index = 1

            while self.vision.what_is_seen()[eye_index] != VisionObject.TAPE:
                self.start_turn(dir)

            self.movement.hold()
            self.update_space()

            return self.spatial_awareness.get_eyes_posses()[eye_index]

        l1 = slow_and_measure("L")
        self.turn_to(start_angle)

        r1 = slow_and_measure("R")
        self.turn_to(start_angle)

        self.go_distance(100)

        l2 = slow_and_measure("L")
        l2.Y += 100
        self.turn_to(start_angle)

        r2 = slow_and_measure("R")
        r2.Y += 100
        self.turn_to(start_angle)


        tape = Road(l1, l2, r1, r2)
        closest_point = tape.mid_fun.closest_point(self.spatial_awareness.cur_position)

        v = self.spatial_awareness.cur_position.to_vector(closest_point)
        a = Trigonometry.calc_angle(v)
        d = self.spatial_awareness.cur_position.dist(closest_point)

        self.turn_to(a)
        self.go_distance(d)

        self.turn_to(tape.mid_fun.angle)
        return tape.mid_fun.angle





    ########################## utils ##########################

    def start_forward(self):
        self.movement.start_forward()
        self.update_space()

    def hold(self):
        self.movement.hold()
        self.update_space()

    def start_turn(self, dir):
        self.movement.start_turn(dir)
        self.update_space()

    def update_space(self):
        self.spatial_awareness.update(self.movement.distance(), self.compass.direction())

    def turn_to(self, correct_angle):
        correct_angle += (self.compass.heading_threshold/2)
        error_direction : Direction = Trigonometry.get_direction(self.compass.calc_error(correct_angle))

        while self.compass.angle_needs_correcting(correct_angle):
            self.start_turn(error_direction)

        self.movement.hold()

    def go_distance(self, distance):
        """
            Drive forward a given distance

            Arguments:
            distance (int): Distance (in mm) that the robot should go forward in
        """
        start_distance = self.movement.distance()
        while self.movement.distance() - start_distance < distance:
            self.start_forward()
            pass
        self.hold()
        self.update_space()

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
