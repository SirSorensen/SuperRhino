from bfs import bfs

class Labyrinth:
    def __init__(self, robot_coordinates : tuple[int, int]):

        self.robot_coordinates = robot_coordinates

        self.distances = { # in cm
            # 0 on Y-axis
            ((0,0) , (1,0)) : 51.5,
            ((0,0) , (0,1)) : 14.6,

            ((1,0) , (2,0)) : 54,
            ((1,0) , (1,1)) : 16.4,

            ((2,0) , (3,0)) : 60,
            ((2,0) , (2,1)) : 16.5,

            ((3,0) , (3,1)) : 16,

            # 1 on Y-axis
            ((0,1) , (1,1)) : 51.7,
            ((0,1) , (0,2)) : 15.5,

            ((1,1) , (2,1)) : 54.5,
            ((1,1) , (1,2)) : 15.3,

            ((2,1) , (3,1)) : 59.2,
            ((2,1) , (2,2)) : 15.1,

            ((3,1) , (3,2)) : 16,

            # 2 on Y-axis
            ((0,2) , (1,2)) : 51.5,
            ((0,2) , (0,3)) : 15.4,

            ((1,2) , (2,2)) : 54.5,
            ((1,2) , (1,3)) : 14.5,

            ((2,2) , (3,2)) : 59.1,
            ((2,2) , (2,3)) : 14.6,

            ((3,2) , (3,3)) : 15.1,

            # 3 on Y-axis
            ((0,3) , (1,3)) : 51.7,

            ((1,3) , (2,3)) : 54.7,

            ((2,3) , (3,3)) : 58.6,
        }

        for (s, e), value in self.distances.items():
            self.distances[(e,s)] = value

        self.tape_distance = 4.7

    def does_path_exist(self, start : tuple[int, int], end : tuple[int, int]) -> bool:
        return (start, end) in self.distances.keys()

    def get_distance(self, start : tuple[int, int], end : tuple[int, int]) -> int:
        if not self.does_path_exist(start, end):
            raise ValueError(f"There is no path from {start} to {end}.")

        return self.distances[(start, end)] + self.tape_distance

    def get_direction(self, start : tuple[int, int], end : tuple[int, int]) -> str:
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

    def get_path(self, start : tuple[int, int], end : tuple[int, int]):
        return bfs(4, 4, start, end)



