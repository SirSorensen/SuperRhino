class CardinalDirection:
    """Robot orientation in a 2D-space"""

    N: tuple[int, int] = (0, 1)
    S: tuple[int, int] = (0, -1)
    W: tuple[int, int] = (-1, 0)
    E: tuple[int, int] = (1, 0)
    CAN: bool = True

    def to_cardinal_direction(s: str):
        if s.upper() == "U" or s.upper() == "N":
            return CardinalDirection.N
        if s.upper() == "D" or s.upper() == "S":
            return CardinalDirection.S
        if s.upper() == "L" or s.upper() == "W":
            return CardinalDirection.W
        if s.upper() == "R" or s.upper() == "E":
            return CardinalDirection.E
        if s.upper() == "C":
            return CardinalDirection.CAN

        raise KeyError("ERROR : Illegal move string!")

    def get_opposite(cd):
        if cd == CardinalDirection.N:
            return CardinalDirection.S

        if cd == CardinalDirection.S:
            return CardinalDirection.N

        if cd == CardinalDirection.W:
            return CardinalDirection.E

        if cd == CardinalDirection.E:
            return CardinalDirection.W


def to_angle(dir: CardinalDirection):
    if dir == CardinalDirection.E:
        return 0
    elif dir == CardinalDirection.N:
        return 270
    elif dir == CardinalDirection.W:
        return 180
    elif dir == CardinalDirection.S:
        return 90

    raise KeyError("ERROR : Illegal cardinal direction!")
