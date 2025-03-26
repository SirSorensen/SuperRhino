
class Measurements:
    def __init__(self):
        temp_edge_lengths = {  # in cm
            # 0 on Y-axis
            ((0, 0), (0, 1)): 51.5,
            ((0, 0), (1, 0)): 14.6,
            ((0, 1), (0, 2)): 54,
            ((0, 1), (1, 1)): 16.4,
            ((0, 2), (0, 3)): 60,
            ((0, 2), (1, 2)): 16.5,
            ((0, 3), (1, 3)): 16,
            # 1 on Y-axis
            ((1, 0), (1, 1)): 51.7,
            ((1, 0), (2, 0)): 15.5,
            ((1, 1), (1, 2)): 54.5,
            ((1, 1), (2, 1)): 15.3,
            ((1, 2), (1, 3)): 59.2,
            ((1, 2), (2, 2)): 15.1,
            ((1, 3), (2, 3)): 16,
            # 2 on Y-axis
            ((2, 0), (2, 1)): 51.5,
            ((2, 0), (3, 0)): 15.4,
            ((2, 1), (2, 2)): 54.5,
            ((2, 1), (3, 1)): 14.5,
            ((2, 2), (2, 3)): 59.1,
            ((2, 2), (3, 2)): 14.6,
            ((2, 3), (3, 3)): 15.1,
            # 3 on Y-axis
            ((3, 0), (3, 1)): 51.7,
            ((3, 1), (3, 2)): 54.7,
            ((3, 2), (3, 3)): 58.6,
        }

        # For each (s,e) key create (e,s) key with same value
        self.edge_lengths = {}
        for (s, e), value in temp_edge_lengths.items():
            self.edge_lengths[(s, e)] = value
            self.edge_lengths[(e, s)] = value

        self.tape_distance = 4.7

    def get_dist(self, s, e):
        return (self.edge_lengths[(s, e)] + self.tape_distance) * 10

    def get_push_dist(self, s, e):
        return (self.edge_lengths[(s, e)]) * 10