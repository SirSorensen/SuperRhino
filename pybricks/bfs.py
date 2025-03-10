
class Queue:
    def __init__(self, start):
        self.list = [start]
        self.index = 0

    def append(self, value):
        self.list.append(value)

    def dequeue(self):
        if self.index >= len(self.list):
            raise ValueError("Queue empty")

        result = self.list[self.index]
        self.index += 1
        return result


def bfs(grid_size_x, grid_size_y, start, end):
    # Possible moves: right, left, down, up
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = Queue((start, [start]))
    visited = set()  # Track visited positions

    while queue:
        (x, y), path = queue.dequeue()

        # If we reached the target, return the path
        if (x, y) == end:
            return path

        # Explore all possible adjacent moves
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # New position

            # Check if the move is within bounds and not visited
            if 0 <= nx < grid_size_x and 0 <= ny < grid_size_y and (nx, ny) not in visited:
                visited.add((nx, ny))
                next = ((nx, ny), path + [(nx, ny)])
                queue.append(next)  # Add new path

    return None  # No path found
