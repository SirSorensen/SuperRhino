


class RobotMeasurer:
    def __init__(self):
        self.measuring_tape_left = False
        self.tape_start_left = 0

        self.measuring_tape_right = False
        self.tape_start_right = 0

    def start_tape_measurement_left(self, current_distance):
        self.measuring_tape_left = True
        self.tape_start_left = current_distance

    def end_tape_measurement_left(self, current_distance):
        self.measuring_tape_left = False
        result = current_distance - self.tape_start_left
        self.tape_start_left = 0
        return result