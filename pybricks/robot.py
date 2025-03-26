from pybricks.parameters import Direction
from pybricks.parameters import Port
from pybricks.hubs import PrimeHub
from pybricks.tools import wait

from mind.spatial_awareness import Spatial_Awareness
from mind.planner import Planner

from utils.point import Point
from utils.cardinal_direction import CardinalDirection
from utils.road import Road
from utils.angle_utils import Angle_Utils
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
        self.spatial_awareness: Spatial_Awareness = Spatial_Awareness((45, 50)) # x = front distance from center, y = side distance from center

    def sokoban(self, solution_str: str):
        self.tape_mid = None

        self.planner: Planner = Planner(solution_str)

        while not self.planner.is_done():
            next_move = self.planner.next_move()
            print("\nNext move =", next_move, end="\n\n")

            if next_move == CardinalDirection.CAN:
                print("CAN!")
                next_move = self.planner.next_move()


            # Turn correct way
            turn_degrees = self.spatial_awareness.next_angle(next_move)
            print(f"Gotta turn {turn_degrees} degrees", end="\n\n")
            self.movement.turn_degrees(turn_degrees)

            # Go forward
            self.goto_next_intersection()

    def goto_next_intersection(self):
        self.tape_mid = self.follow_tape()
        print(f"Got mid_tape! correct_angle:{self.tape_mid.mid_angle} \n -> current_angle:{self.compass.direction()}")

        self.go_to_point(self.tape_mid.front_center)
        self.turn_to(self.tape_mid.mid_angle)

        while True:
            # PID
            self.start_forward()
            if self.compass.angle_needs_correcting(self.tape_mid.mid_angle):
                self.hold()
                self.turn_to(self.tape_mid.mid_angle)




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
            result = self.spatial_awareness.get_eyes_posses(self.compass.direction())[eye_index]
            print(f"slow_and_measure({side}) => {result}", end="\n\n")
            self.turn_to(start_angle)
            wait(500)
            return result

        print("cur_pos =", self.spatial_awareness.cur_position)
        l1 = slow_and_measure("L")
        r1 = slow_and_measure("R")
        self.go_distance(100)
        print("cur_pos =", self.spatial_awareness.cur_position)
        l2 = slow_and_measure("L")
        r2 = slow_and_measure("R")
        self.go_distance(100)
        l3 = slow_and_measure("L")
        r3 = slow_and_measure("R")
        return Road(l1, l2, l3, r1, r2, r3)


    ########################## utils ##########################

    def start_forward(self):
        self.movement.start_forward()
        self.update_space()

    def hold(self):
        self.movement.hold()
        self.update_space()

    def start_turn(self, dir):
        self.movement.start_turn(dir)

    def update_space(self):
        self.spatial_awareness.update(self.movement.distance(), self.compass.direction())

    def turn_to(self, correct_angle):
        correct_angle += self.compass.heading_threshold / 2
        error_direction: Direction = Angle_Utils.get_direction(self.compass.calc_error(correct_angle))

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