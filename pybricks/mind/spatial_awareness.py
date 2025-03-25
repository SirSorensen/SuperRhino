class Spatial_Awareness:
    def __init__(self, start_direction: str):
        self.cur_direction: str = start_direction
        print("Starting values:")
        print(self.cur_direction)

    def cur_angle(self):
        return self.cur_direction

    def update_state(self):
        #TODO: FIGURE OUT STATE / DIRECTION
        pass

    def update_space(self):
        #TODO: FIGURE OUT SPACE
        pass

    def next_angle(self, move) -> float:
        # TODO: Take move and return next direction
        result: tuple[float, float] = 0

        print("Next values:")
        print("Direction =", self.cur_direction)
        return result
