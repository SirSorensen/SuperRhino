from pybricks.parameters import Direction
from pybricks.parameters import Port
from pybricks.hubs import PrimeHub
from pybricks.tools import wait

from mind.spatial_awareness import Spatial_Awareness
from mind.planner import Planner

from utils.point import Point
from utils.cardinal_direction import CardinalDirection, to_angle
from utils.road import Road
from utils.angle_utils import Angle_Utils
from utils.state import VisionObject
from senses.vision import Vision
from senses.compass import Compass

from physiology.movement import Movement


print_method_calls = True


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
        self.spatial_awareness: Spatial_Awareness = Spatial_Awareness((45, 50)) # x = front distance from center, y = side distance from center

    def sokoban(self, solution_str: str):
        self.planner: Planner = Planner(solution_str)

        while not self.planner.is_done():
            next_move = self.planner.next_move()
            print(f"\n\n\n ################ NEW MOVE ({next_move}) ################")
            print("\nNext move =", next_move, end="\n\n")

            while next_move == CardinalDirection.CAN:
                print("CAN!")
                next_move = self.planner.next_move()


            # Turn correct way
            turn_degrees = self.spatial_awareness.next_angle(next_move)
            self.turn_to(turn_degrees)

            # Go forward
            self.goto_next_intersection()

    def goto_next_intersection(self):
        self.tape_mid = self.follow_tape()
        print(f"Got mid_tape! correct_angle:{self.tape_mid.mid_angle} \n -> current_angle:{self.compass.direction()}")

        self.tape_counter = 0
        self.tape_start = (None, None)
        self.tape_end = (None, None)

        while True:
            # PID
            self.start_forward(self.tape_mid.mid_angle)
            if self.detect_intersection():
                return



    def detect_intersection(self):
        if self.do_i_see_tape():
            self.set_tape_start()
            self.tape_counter += 1 # For resetting tape_start
        else:
            if self.get_max_tape_dist() >= 47: # max seen = 50.05484
                self.hold()
                self.set_tape_end()
                closest_point = self.set_intersection_mid()
                self.go_to_point(closest_point)
                return True


            self.tape_counter = max(0, self.tape_counter - 5) # For resetting tape_start
            if self.tape_counter == 0: # For resetting tape_start
                self.tape_start = (None, None) # For resetting tape_start

    def do_i_see_tape(self):
        left_obj, right_obj = self.vision.what_is_seen()
        return left_obj == VisionObject.TAPE or right_obj == VisionObject.TAPE

    def set_tape_start(self):
        left_start, right_start = self.tape_start
        if left_start is None or right_start is None:
            left_obj, right_obj = self.vision.what_is_seen()
            left_eye_pos, right_eye_pos = self.cur_direction()

            if left_start is None and left_obj == VisionObject.TAPE:
                left_start = left_eye_pos
            if right_start is None and right_obj == VisionObject.TAPE:
                right_start = right_eye_pos
        self.tape_start = (left_start, right_start)


    def set_tape_end(self):
        left_start, right_start = self.tape_start
        left_end, right_end = (None, None)
        left_obj, right_obj = self.vision.what_is_seen()
        left_eye_pos, right_eye_pos = self.cur_direction()

        if left_start is not None and left_obj == VisionObject.TABLE:
            left_end = left_eye_pos
        if right_start is not None and right_obj == VisionObject.TABLE:
            right_end = right_eye_pos
        self.tape_end = (left_end, right_end)


    def set_intersection_mid(self):
        left_start, right_start = self.tape_start
        left_end, right_end = self.tape_end

        if left_end is not None:
            print(f"left_start:{left_start}, left_end:{left_end}")
            left_mid = left_start.mid_point(left_end)
            mid = left_mid
        if right_end is not None:
            print(f"right_start:{right_start}, right_end:{right_end}")
            right_mid = right_start.mid_point(right_end)
            mid = right_mid

        if left_end is not None and right_end is not None:
            mid = left_mid.mid_point(right_mid)


        return self.tape_mid.closest_point(mid)


    def get_max_tape_dist(self):
        if self.tape_start is None or self.tape_start == (None, None):
            return 0

        eye_poses = self.cur_direction()

        if self.tape_start[0] is not None and self.tape_start[1] is not None:
            return max(self.tape_start[0].dist(eye_poses[0]), self.tape_start[1].dist(eye_poses[1]))
        elif self.tape_start[0] is not None:
            return self.tape_start[0].dist(eye_poses[0])
        else:
            return self.tape_start[1].dist(eye_poses[1])




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

            self.hold()
            self.update_space()
            result = self.cur_direction()[eye_index]
            print(f"slow_and_measure({side}) => {result}", end="\n\n")
            self.turn_to(start_angle)
            wait(500)
            return result

        print("cur_pos =", self.spatial_awareness.cur_position)
        wait(500)
        l1 = slow_and_measure("L")
        r1 = slow_and_measure("R")
        self.go_distance(50)
        print("cur_pos =", self.spatial_awareness.cur_position)
        l2 = slow_and_measure("L")
        r2 = slow_and_measure("R")
        self.go_distance(50)
        l3 = slow_and_measure("L")
        r3 = slow_and_measure("R")
        self.go_distance(-100)
        return Road(l1, l2, l3, r1, r2, r3)


    ########################## utils ##########################

    def start_forward(self, correct_angle):
        if self.compass.angle_needs_correcting(correct_angle, 3):
            self.hold()
            self.turn_to(correct_angle)
        else:
            self.movement.start_forward()
            self.update_space()

    def hold(self):
        self.movement.hold()
        wait(500)
        self.update_space()

    def start_turn(self, dir, magnitude = 1):
        self.movement.start_turn(dir, magnitude)

    def update_space(self):
        self.spatial_awareness.update(self.movement.distance(), self.compass.direction())

    def turn_to(self, correct_angle):
        print(f"Gotta turn to {correct_angle}", end="\n\n")
        error_direction: Direction = Angle_Utils.get_direction(correct_angle - self.compass.direction())

        while self.compass.angle_needs_correcting(correct_angle, 2):
            self.start_turn(error_direction)
        while self.compass.angle_needs_correcting(correct_angle, 1):
            self.start_turn(error_direction, 0.75)

        self.hold()

    def go_distance(self, distance):
        """
        Drive forward a given distance

        Arguments:
        distance (int): Distance (in mm) that the robot should go forward in
        """
        start_distance = self.movement.distance()
        if distance > 0:
            while self.movement.distance() - start_distance < distance:
                self.movement.start_forward()
        elif distance < 0:
            while self.movement.distance() - start_distance > distance:
                self.movement.start_forward(-1)
        self.hold()

    def go_to_point(self, point : Point):
        print(f"Going to point {point}")
        dir_vector = self.spatial_awareness.cur_position.to_vector(point)
        degrees = dir_vector.degrees()
        print(f"Turning to {degrees}")
        self.turn_to(degrees)
        wait(500)
        print(f"Going {dir_vector.length()}")
        self.go_distance(dir_vector.length())
        wait(500)

    def cur_direction(self):
        return self.spatial_awareness.get_eyes_posses(self.compass.direction())