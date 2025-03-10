from bfs import sokuban_bfs


class Labyrinth:
    def __init__(
        self, robot_coordinates: tuple[int, int], cans: list[tuple[int, int]] = []
    ):

        self.robot_coordinates = robot_coordinates

        self.edge_lengths = {  # in cm
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
        for (s, e), value in self.edge_lengths.items():
            self.edge_lengths[(e, s)] = value

        self.tape_distance = 4.7

        # Can coordinates
        self.cans = cans

    def does_edge_exist(self, start: tuple[int, int], end: tuple[int, int]) -> bool:
        return (start, end) in self.edge_lengths.keys()

    def get_distance(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        if not self.does_edge_exist(start, end):
            raise ValueError(f"There is no path from {start} to {end}.")

        return self.edge_lengths[(start, end)] + self.tape_distance

    def get_direction(self, start: tuple[int, int], end: tuple[int, int]) -> str:
        (sx, sy) = start
        (ex, ey) = end

        if sx < ex and sy == ey:
            return "RIGHT"
        elif sx > ex and sy == ey:
            return "LEFT"
        elif sx == ex and sy < ey:
            return "UP"
        elif sx == ex and sy > ey:
            return "DOWN"

        return ""

    def parse_sokoban_map(map_str):
        grid = [list(row) for row in map_str.strip().split("\n")]
        return grid

    def find_positions(grid):
        rhinotron = None
        cans = set()
        goals = set()

        for y, row in enumerate(grid):
            for x, point in enumerate(row):
                if point == "@":
                    rhinotron = (x, y)
                elif point == "$":
                    cans.add((x, y))
                elif point == ".":
                    goals.add((x, y))
                elif point == "*":
                    cans.add((x, y))
                    goals.add((x, y))

        return rhinotron, cans, goals

    def is_valid_can_move(point, new_point):
        x, y = point
        nx, ny = new_point

        if abs(x - nx) <= 1 and abs(y - ny) <= 1:
            return True

    def get_path(self, start: tuple[int, int], end: tuple[int, int]):
        return sokuban_bfs(4, 4, start, end, self.cans)
