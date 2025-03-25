from pybricks.parameters import Direction
import umath as math

from physiology.movement import Movement
from senses.utils.angle import Angle
from senses.vision import Vision
from senses.compass import Compass


def go(movement: Movement, compass: Compass, turn_degree, move_dist):
    compass.reset()

    movement.turn_to(turn_degree)
    fix_angle(movement, compass, turn_degree)

    movement.reset_distance()
    compass.reset()
    while movement.get_distance() < move_dist:
        movement.start_forward()
        movement, compass = fix_angle(movement, compass, 0)

    return movement, compass


def fix_angle(movement: Movement, compass: Compass, correct_angle):
    dir_error = compass.calc_direction_error(correct_angle)
    if dir_error != 0:
        movement.hold()

    while dir_error != 0:
        movement.turn_to(dir_error)
        dir_error = compass.calc_direction_error(correct_angle)

    return movement, compass


def measure_tape(movement: Movement, compass: Compass, vision: Vision, camera_dist: float, angle_to_camera: float):
    def slow_and_measure(side: str):
        if side.upper() == "L":
            dir = Direction.COUNTERCLOCKWISE
            eye_index = 0
            fix_angle = -angle_to_camera
        else:
            dir = Direction.CLOCKWISE
            eye_index = 1
            fix_angle = angle_to_camera

        movement.start_turn(dir)
        while vision.what_is_seen()[eye_index] != "TAPE":
            pass
        movement.hold()
        tape_edge_angle = compass.direction() + fix_angle
        return (math.cos(tape_edge_angle), math.sin(tape_edge_angle))

    compass.reset()  # Direction = 0 degrees

    l1 = slow_and_measure("L")
    fix_angle(movement, compass, 0)
    r1 = slow_and_measure("R")
    fix_angle(movement, compass, 0)

    movement.go_distance(100)

    l2_x, l2_y = slow_and_measure("L")
    l2_y += 100
    fix_angle(movement, compass, 0)
    r2_x, r2_y = slow_and_measure("R")
    r2_y += 100

    fix_angle(movement, compass, 0)

    def calc_line_degree(point_1, point_2):
        x1, y1 = point_1
        x2, y2 = point_2
        f = (y2 - y1) / (x2 - x1)
        line_length = math.sqrt(f**2 + 1**2)
        normalized = f / line_length
        return Angle.to_angle_from_radians(math.asin(normalized))

    l_angle = calc_line_degree(l1, (l2_x, l2_y))
    r_angle = calc_line_degree(r1, (r2_x, r2_y))
    avg_angle = (l_angle + r_angle) / 2
    angle_error = Angle.calc_error(avg_angle, 0)

    fix_angle(movement, compass, angle_error)

    x_error = (r2_x + l2_x) / 2
    if x_error > 0:
        movement.turn_to(90)
        movement.go_distance(x_error)
        movement.turn_to(-90)
    else:
        movement.turn_to(-90)
        movement.go_distance(x_error)
        movement.turn_to(90)

    fix_angle(movement, compass, angle_error)
