class CardinalDirection:
    """Robot orientation in a 2D-space"""

    N: tuple[int, int] = (0, 1)
    S: tuple[int, int] = (0, -1)
    W: tuple[int, int] = (-1, 0)
    E: tuple[int, int] = (1, 0)

    def to_cardinal_direction(s: str):
        if s.upper() == "U" or s.upper() == "N":
            return CardinalDirection.N
        if s.upper() == "D" or s.upper() == "S":
            return CardinalDirection.S
        if s.upper() == "L" or s.upper() == "W":
            return CardinalDirection.W
        if s.upper() == "R" or s.upper() == "E":
            return CardinalDirection.E

        raise KeyError("ERROR : Illegal move string!")


def diff(cur_dir: CardinalDirection, next_dir: CardinalDirection):
    if cur_dir == next_dir:
        return 0
    if (cur_dir, next_dir) == (CardinalDirection.N, CardinalDirection.S) or (cur_dir, next_dir) == (CardinalDirection.E, CardinalDirection.W) or (cur_dir, next_dir) == (CardinalDirection.S, CardinalDirection.N) or (cur_dir, next_dir) == (CardinalDirection.W, CardinalDirection.E):
        return 180
    if (cur_dir, next_dir) == (CardinalDirection.N, CardinalDirection.E) or (cur_dir, next_dir) == (CardinalDirection.E, CardinalDirection.S) or (cur_dir, next_dir) == (CardinalDirection.S, CardinalDirection.W) or (cur_dir, next_dir) == (CardinalDirection.W, CardinalDirection.N):
        return 90
    if (cur_dir, next_dir) == (CardinalDirection.N, CardinalDirection.W) or (cur_dir, next_dir) == (CardinalDirection.E, CardinalDirection.N) or (cur_dir, next_dir) == (CardinalDirection.S, CardinalDirection.E) or (cur_dir, next_dir) == (CardinalDirection.W, CardinalDirection.S):
        return -90

    raise KeyError("ERROR : Illegal orientations!")
