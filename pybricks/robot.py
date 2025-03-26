from pybricks.parameters import Direction
from pybricks.parameters import Port
from pybricks.hubs import PrimeHub
from pybricks.tools import wait

from mind.spatial_awareness import Spatial_Awareness
from mind.planner import Planner

from utils.cardinal_direction import CardinalDirection
from utils.road import Road
from utils.trigonometry import Angle_Utils
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

        while True:
            # PID
            self.start_forward()




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
            return self.spatial_awareness.get_eyes_posses(self.compass.direction())[eye_index]


        print("cur_pos =", self.spatial_awareness.cur_position)
        l1 = slow_and_measure("L")
        print("l1 =", l1)
        self.turn_to(start_angle)
        wait(500)

        r1 = slow_and_measure("R")
        print("r1 =", r1)
        self.turn_to(start_angle)
        wait(500)
        print("\n")

        self.go_distance(150)

        wait(500)
        print("cur_pos =", self.spatial_awareness.cur_position)
        l2 = slow_and_measure("L")
        print("l2 =", l2)
        self.turn_to(start_angle)
        wait(500)

        r2 = slow_and_measure("R")
        print("r2 =", r2)
        self.turn_to(start_angle)
        wait(500)
        print("\n")

        tape = Road(l1, l2, r1, r2)
        self.turn_to(tape.mid_angle)

        return tape


    ########################## utils ##########################

    def start_forward(self):
        if self.tape_mid is None:
            self.movement.start_forward()
        else:
            err = self.tape_mid.diff(self.spatial_awareness.cur_position)
            self.movement.start_forward(err)
        self.update_space()
        wait(50)

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