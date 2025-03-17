from physiology.movement import Movement
from senses.compass import Compass


def go(movement: Movement, compass: Compass, turn_degree, move_dist):
    compass.reset()

    movement.turn(turn_degree)
    fix_angle(movement, compass, turn_degree)

    movement.reset_distance()
    compass.reset()
    while movement.get_distance() < move_dist:
        movement.go_forward()
        movement, compass = fix_angle(movement, compass, 0)

    return movement, compass


def fix_angle(movement: Movement, compass: Compass, correct_angle):
    dir_error = compass.calc_direction_error(correct_angle)
    if dir_error != 0:
        movement.hold()

    while dir_error != 0:
        movement.turn(dir_error)
        dir_error = compass.calc_direction_error(correct_angle)

    return movement, compass
