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
        self.spatial_awareness: Spatial_Awareness = Spatial_Awareness((2, 4))  # TODO: Measure dist to eyes

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
        self.tape_mid = self.follow_tape()
        correct_angle = self.tape_mid.angle
        self.tape_counter = 0
        self.tape_start = None
        self.tape_end = None
        self.intersection_mid = None
        self.end_point = None

        while True:
            self.movement.start_forward()

            # PID
            if self.compass.angle_needs_correcting(correct_angle):
                self.hold()
                self.turn_to(correct_angle)
                self.start_forward()

            # I see not table!
            self.detect_intersection()
            if self.end_point is not None and self.spatial_awareness.cur_position.dist(self.end_point) <= 0.1:
                self.hold()
                return



    def detect_intersection(self):
        if self.vision.what_is_seen()[0] == VisionObject.TAPE or self.vision.what_is_seen()[1] == VisionObject.TAPE:
            if self.tape_counter == 0:
                self.tape_start = self.get_vision(VisionObject.TAPE)
            self.tape_counter += 1
        else:
            if self.get_max_tape_dist() >= 47:
                self.tape_end = self.get_vision(VisionObject.TABLE)
                if self.tape_start[0] is None:
                    self.tape_end[0] = None
                if self.tape_start[1] is None:
                    self.tape_end[1] = None
                self.end_point = self.calc_intersection_mid()

            tape_counter = max(0, self.tape_counter - 1)
            if tape_counter == 0:
                self.tape_start = (None, None)

    def get_vision(self, vision_object):
        if self.vision.what_is_seen() == (vision_object, vision_object):
            return self.spatial_awareness.get_eyes_posses()
        elif self.vision.what_is_seen()[0] == vision_object:
            return (self.spatial_awareness.get_eyes_posses()[0], None)
        else:
            return (None, self.spatial_awareness.get_eyes_posses()[1])


    def get_max_tape_dist(self):
        if self.tape_start == (None, None):
            return 0

        eye_poses = self.spatial_awareness.get_eyes_posses()

        if self.tape_start[0] is not None and self.tape_start[1] is not None:
            return max(self.tape_start[0].dist(eye_poses[0]), self.tape_start[1].dist(eye_poses[1]))
        elif self.tape_start[0] is not None:
            return self.tape_start[0].dist(eye_poses[0])
        else:
            return self.tape_start[1].dist(eye_poses[1])


    def calc_intersection_mid(self):
        left_start, right_start = self.tape_start
        left_end, right_end = self.tape_end
        if left_start is not None and left_end is not None:
            left_mid = left_start.mid_point(left_end)
        else:
            left_mid = None

        if right_start is not None and right_end is not None:
            right_mid = right_start.mid_point(right_end)
        else:
            right_mid = None

        if left_mid is None and right_mid is None:
            raise ValueError("Left mid and right mid is None")

        if left_mid is not None and right_mid is not None:
            mid = left_mid.mid_point(right_mid)
        elif left_mid is not None:
            mid = left_mid
        else:
            mid = right_mid

        return self.tape_mid.closest_point(mid)




    def follow_tape(self):
        start_angle = self.compass.direction()

        def slow_and_measure(side : str):
            if side.upper() == "L":
                dir = Direction.CLOCKWISE
                eye_index = 0
            else:
                dir = Direction.COUNTERCLOCKWISE
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
        return tape.mid_fun


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
        self.spatial_awareness.print_status()

    def turn_to(self, correct_angle):
        correct_angle += self.compass.heading_threshold / 2
        error_direction: Direction = Trigonometry.get_direction(self.compass.calc_error(correct_angle))

        while self.compass.angle_needs_correcting(correct_angle):
            self.start_turn(error_direction)

        self.hold()

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
