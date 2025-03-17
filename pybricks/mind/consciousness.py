

class Consciousness:
    def __init__(self, start_direction : str, start_position : tuple[int, int]):
        temp_edge_lengths = {  # in cm
            # 0 on Y-axis
            ((0, 0), (1, 0)): 51.5,
            ((0, 0), (0, 1)): 14.6,
            ((1, 0), (2, 0)): 54,
            ((1, 0), (1, 1)): 16.4,
            ((2, 0), (3, 0)): 60,
            ((2, 0), (2, 1)): 16.5,
            ((3, 0), (3, 1)): 16,
            # 1 on Y-axis
            ((0, 1), (1, 1)): 51.7,
            ((0, 1), (0, 2)): 15.5,
            ((1, 1), (2, 1)): 54.5,
            ((1, 1), (1, 2)): 15.3,
            ((2, 1), (3, 1)): 59.2,
            ((2, 1), (2, 2)): 15.1,
            ((3, 1), (3, 2)): 16,
            # 2 on Y-axis
            ((0, 2), (1, 2)): 51.5,
            ((0, 2), (0, 3)): 15.4,
            ((1, 2), (2, 2)): 54.5,
            ((1, 2), (1, 3)): 14.5,
            ((2, 2), (3, 2)): 59.1,
            ((2, 2), (2, 3)): 14.6,
            ((3, 2), (3, 3)): 15.1,
            # 3 on Y-axis
            ((0, 3), (1, 3)): 51.7,
            ((1, 3), (2, 3)): 54.7,
            ((2, 3), (3, 3)): 58.6,
        }

        # For each (s,e) key create (e,s) key with same value
        self.edge_lengths = {}
        for (s, e), value in temp_edge_lengths.items():
            sx, sy = s
            transformed_s = (sy, 3 - sx)
            ex, ey = e
            transformed_e = (ey, 3 - ex)
            self.edge_lengths[(transformed_s, transformed_e)] = value
            self.edge_lengths[(transformed_e, transformed_s)] = value

        self.tape_distance = 4.7

        self.cur_direction : str = start_direction
        self.cur_position : tuple[int, int] = start_position
        print("Starting values:")
        print(self.cur_direction)
        print(self.cur_position)

    def which_way_am_i_pointing(self):
        return self.cur_direction

    def where_am_i(self):
        return self.cur_position

    def change_state(self, move : str):
        self.cur_direction = self.next_direction(move)
        self.cur_position = self.next_position(move)

    def next_direction(self, move : str):
        if move.upper() == "U":
            return "N"
        if move.upper() == "D":
            return "S"
        if move.upper() == "L":
            return "W"
        if move.upper() == "R":
            return "E"

        print("ERROR : Illegal move string!")
        return self.cur_direction

    def next_position(self, move : str):
        x, y = self.cur_position

        if move.upper() == "U":
            return (x, y+1)
        if move.upper() == "D":
            return (x, y-1)
        if move.upper() == "L":
            return (x-1, y)
        if move.upper() == "R":
            return (x+1, y)

        print("ERROR : Illegal move string!")
        return self.cur_position

    def move_distance(self, move : str):
        s = self.cur_position
        e = self.next_position(move)
        return self.edge_lengths[(s,e)] + self.tape_distance

    def turn_degree(self, move : str):
        cur_dir = self.cur_direction
        next_dir = self.next_direction(move)
        if (cur_dir, next_dir) == ("N", "S"):
            return 180
        if (cur_dir, next_dir) == ("E", "W"):
            return 180
        if (cur_dir, next_dir) == ("S", "N"):
            return 180
        if (cur_dir, next_dir) == ("W", "E"):
            return 180
        if (cur_dir, next_dir) == ("N", "E"):
            return 90
        if (cur_dir, next_dir) == ("E", "S"):
            return 90
        if (cur_dir, next_dir) == ("S", "W"):
            return 90
        if (cur_dir, next_dir) == ("W", "N"):
            return 90
        if (cur_dir, next_dir) == ("N", "W"):
            return -90
        if (cur_dir, next_dir) == ("E", "N"):
            return -90
        if (cur_dir, next_dir) == ("S", "E"):
            return -90
        if (cur_dir, next_dir) == ("W", "S"):
            return -90
        if (cur_dir, next_dir) == ("N", "N"):
            return 0
        if (cur_dir, next_dir) == ("E", "E"):
            return 0
        if (cur_dir, next_dir) == ("S", "S"):
            return 0
        if (cur_dir, next_dir) == ("W", "W"):
            return 0

        print("ERROR : Illegal move string!")
        return 0

    def next(self, move : str):
        result = (self.turn_degree(move), self.move_distance(move))
        self.change_state(move)

        print("Next values:")
        print("Direction =", self.cur_direction)
        print("Position =", self.cur_position)
        return result



