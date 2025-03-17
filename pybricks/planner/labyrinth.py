from our_queue import Queue


class Labyrinth:
    def __init__(self):
        pass

    def parse_map_str(map_str: str) -> list[list[str]]:
        grid = [list(row) for row in map_str.strip().split("\n")]
        return grid

    def find_walls(self) -> set[tuple[int,int]]:
        walls = set()
        for y, row in enumerate(self.grid):
            for x, point in enumerate(row):
                if point == "#" or point == "X":
                    walls.add((x, y))
        return walls

    def parse_sokoban_map(self, map_str) -> list[list[str]]:
        """Convert a Sokoban map string into a 2D grid representation."""
        grid = [list(row) for row in map_str.strip().split("\n")]
        return grid

    def find_positions(self, grid) -> tuple[None|tuple[int, int],set[tuple[int,int]],set[tuple[int,int]]]:
        """Find the player, boxes, and goal positions."""
        rhinotron = None
        cans = set()
        goals = set()

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == "@":  # Player
                    rhinotron = (x, y)
                elif cell == "$":  # Box
                    cans.add((x, y))
                elif cell == ".":  # Goal
                    goals.add((x, y))
                elif cell == "*":  # Box on goal
                    cans.add((x, y))
                    goals.add((x, y))
                elif cell == "+":  # Player on goal
                    rhinotron = (x, y)
                    goals.add((x, y))

        return rhinotron, cans, goals

    def is_valid_move(self, grid, pos) -> bool:
        """Check if a move is valid (not a wall)."""
        x, y = pos
        return grid[y][x] not in ("#")

    def is_valid_push(self, grid, box_pos, direction) -> bool:
        """Check if pushing a box in a direction is possible."""
        x, y = box_pos
        dx, dy = direction
        new_x, new_y = x + dx, y + dy

        if grid[new_y][new_x] in ("#", "$"):  # Can't push into walls or another box
            return False
        return True

    def sokoban_solver(self, grid) -> str:
        """Solve Sokoban using BFS."""
        player, boxes, goals = self.find_positions(grid)
        directions = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}

        queue = Queue()
        queue.enqueue((player, frozenset(boxes), ""))  # Start BFS
        visited = set()

        while queue:
            player, boxes, moves = queue.dequeue()

            # If all boxes are on goals, return solution
            if boxes == goals:
                return moves

            if (player, boxes) in visited:
                continue
            visited.add((player, boxes))

            # Try moving the player in each direction
            for move, (dx, dy) in directions.items():
                new_rhinotron = (player[0] + dx, player[1] + dy)

                # If moving into a box, try pushing it
                if new_rhinotron in boxes:
                    new_can = (new_rhinotron[0] + dx, new_rhinotron[1] + dy)

                    if new_can not in boxes and self.is_valid_push(
                        grid, new_rhinotron, (dx, dy)
                    ):
                        new_boxes = frozenset(
                            (new_can if b == new_rhinotron else b) for b in boxes
                        )
                        queue.enqueue((new_rhinotron, new_boxes, moves + move))
                else:
                    # Move player normally if the space is empty
                    if self.is_valid_move(grid, new_rhinotron):
                        queue.enqueue((new_rhinotron, boxes, moves + move))

        return "No solution"