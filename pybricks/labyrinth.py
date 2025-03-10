from bfs import sokuban_bfs, Queue


class Labyrinth:
    def __init__(
        self, map_str : str
    ):

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
            self.edge_lengths[(s, e)] = value
            self.edge_lengths[(e, s)] = value

        self.tape_distance = 4.7

        # Grid init
        self.grid = Labyrinth.parse_map_str(map_str)
        self.walls = self.find_walls()

    def parse_map_str(map_str : str):
        grid = [list(row) for row in map_str.strip().split("\n")]
        return grid

    def find_walls(self):
        walls = set()
        for y, row in enumerate(self.grid):
            for x, point in enumerate(row):
                if point == "#" or point == "X":
                    walls.add((x, y))
        return walls

    def find_positions(self):
        rhinotron = None
        cans = set()
        goals = set()

        for y, row in enumerate(self.grid):
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


    def is_valid_push(walls, cans, push_point):
        if push_point in walls or push_point in cans:
            return False
        return True

    def is_valid_move(walls, moved_point):
        if moved_point in walls:
            return False
        return True

    def solve(self):
        start_rhinotron, start_cans, self.goals = self.find_positions()
        queue = Queue((start_rhinotron, frozenset(start_cans), []))
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        visited = set([])

        while not queue.is_empty():
            print("Items before dequeue:", queue.count())
            rhinotron, cans, moves = queue.dequeue()
            print("Items after dequeue:", queue.count())

            # All cans are in goals

            if len([0 for c in cans if c not in self.goals]) == 0:
                return moves

            # If we have already checked this state, skip
            if (rhinotron, cans) in visited:
                continue


            visited.add((rhinotron, cans))

            # Try moving rhinotron in each direction
            for (dx, dy) in directions:
                # Define next point
                nx = rhinotron[0] + dx
                ny = rhinotron[1] + dy
                new_rhinotron = (nx, ny)

                # Add move to new_moves list
                new_moves = moves + [(dx, dy)]

                if (nx, ny) in cans:
                    # Define new can points
                    new_can_point = (nx + dx, ny + dy)

                    if new_can_point not in cans and Labyrinth.is_valid_push(self.walls, cans, new_can_point):

                        new_cans = frozenset(new_can_point if cur == new_rhinotron else cur for cur in cans)


                        queue.append((new_rhinotron, new_cans, new_moves))

                elif Labyrinth.is_valid_move(self.walls, new_rhinotron):
                    queue.append((new_rhinotron, cans, new_moves))

        return []





map_string = """
########
#@$.   #
#$*$  .#
#.$ *#.#
#  $ $ #
# #$..##
#.. $  #
########
"""

lab = Labyrinth(map_string)

print(lab.solve())