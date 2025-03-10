
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