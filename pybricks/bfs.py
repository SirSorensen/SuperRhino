from collections import deque


def bfs(grid_size, start, end):
    # Possible moves: right, left, down, up
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = deque([(start, [start])])  # (current position, path taken)
    visited = set()  # Track visited positions

    while queue:
        (x, y), path = queue.popleft()

        # If we reached the target, return the path
        if (x, y) == end:
            return path

        # Explore all possible adjacent moves
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # New position

            # Check if the move is within bounds and not visited
            if 0 <= nx < grid_size and 0 <= ny < grid_size and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))  # Add new path

    return None  # No path found


# Example usage
grid_size = 4
start = (0, 0)
end = (3, 3)

shortest_path = bfs(grid_size, start, end)
print("Shortest Path:", shortest_path)
