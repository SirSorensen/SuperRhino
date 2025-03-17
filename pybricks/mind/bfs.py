class Node:
    def __init__(self, value):
        self.next = None
        self.value = value

class Queue:
    def __init__(self, start_value):
        self.front = Node(start_value)
        self.back = self.front

    def append(self, value):
        if self.is_empty():
            self.front = Node(value)
            self.back = self.front
        else:
            self.back.next = Node(value)
            self.back = self.back.next


    def dequeue(self):
        result = self.front.value
        self.front = self.front.next
        return result

    def is_empty(self):
        return self.front is None

    def count(self):
        cur = self.front
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next
        return count


def sokuban_bfs(grid_size_x, grid_size_y, start, end, blocks):
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
            if (
                0 <= nx < grid_size_x
                and 0 <= ny < grid_size_y
                and (nx, ny) not in visited
            ):
                visited.add((nx, ny))
                next = ((nx, ny), path + [(nx, ny)])
                queue.append(next)  # Add new path

    return None  # No path found
