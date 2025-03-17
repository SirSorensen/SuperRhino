from physiology.movement import Movement
from senses.directional import Sense_of_Direction

class Nervous_System:
    def go(movement : Movement, directional : Sense_of_Direction, turn_degree, move_dist):
        directional.reset()

        movement.turn(turn_degree)
        Nervous_System.fix_angle(movement, directional, turn_degree)

        movement.reset_distance()
        directional.reset()
        while movement.get_distance() < move_dist:
            movement.go_forward()
            Nervous_System.fix_angle(movement, directional, 0)


    def fix_angle(movement : Movement, directional : Sense_of_Direction, correct_angle):
        dir_error = directional.calc_direction_error(correct_angle)
        if dir_error != 0:
            movement.hold()
        
        while dir_error != 0:
            movement.turn(dir_error)
            dir_error = directional.calc_direction_error(correct_angle)