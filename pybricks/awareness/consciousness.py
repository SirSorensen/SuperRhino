

class Consciousness:
    def __init__(self, start_direction : str, start_position : tuple[int, int]):
        temp_edge_lengths = {  # in mm
            ((3, 3), (2, 3)): 515,
            ((3, 3), (3, 2)): 146,
            ((2, 3), (1, 3)): 540,
            ((2, 3), (2, 2)): 164,
            ((1, 3), (0, 3)): 600,
            ((1, 3), (1, 2)): 165,
            ((0, 3), (0, 2)): 160,
            ((3, 2), (2, 2)): 517,
            ((3, 2), (3, 1)): 155,
            ((2, 2), (1, 2)): 545,
            ((2, 2), (2, 1)): 153,
            ((1, 2), (0, 2)): 592,
            ((1, 2), (1, 1)): 151,
            ((0, 2), (0, 1)): 160,
            ((3, 1), (2, 1)): 515,
            ((3, 1), (3, 0)): 154,
            ((2, 1), (1, 1)): 545,
            ((2, 1), (2, 0)): 145,
            ((1, 1), (0, 1)): 591,
            ((1, 1), (1, 0)): 146,
            ((0, 1), (0, 0)): 151,
            ((3, 0), (2, 0)): 517,
            ((2, 0), (1, 0)): 547,
            ((1, 0), (0, 0)): 586,
        }

        # For each (s,e) key create (e,s) key with same value
        self.edge_lengths = {}
        for (s, e), value in temp_edge_lengths.items():
            self.edge_lengths[(s, e)] = value
            self.edge_lengths[(e, s)] = value

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
        if (cur_dir, next_dir) == ("N", "S") or (cur_dir, next_dir) == ("E", "W") or (cur_dir, next_dir) == ("S", "N") or (cur_dir, next_dir) == ("W", "E"):
            return 180
        if (cur_dir, next_dir) == ("N", "E") or (cur_dir, next_dir) == ("E", "S") or (cur_dir, next_dir) == ("S", "W") or (cur_dir, next_dir) == ("W", "N"):
            return 90
        if (cur_dir, next_dir) == ("N", "W") or (cur_dir, next_dir) == ("E", "N") or (cur_dir, next_dir) == ("S", "E") or (cur_dir, next_dir) == ("W", "S"):
            return -90
        if (cur_dir, next_dir) == ("N", "N") or (cur_dir, next_dir) == ("E", "E") or (cur_dir, next_dir) == ("S", "S") or (cur_dir, next_dir) == ("W", "W"):
            return 0

        print("ERROR : Illegal move string!")
        return 0

    def next(self, move : str) -> tuple[float, float]:
        result : tuple[float, float] = (self.turn_degree(move), self.move_distance(move))
        self.change_state(move)

        print("Next values:")
        print("Direction =", self.cur_direction)
        print("Position =", self.cur_position)
        return result



