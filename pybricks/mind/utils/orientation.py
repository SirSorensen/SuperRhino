class Orientation:
    """Robot orientation in a 2D-space"""
    N: tuple[int, int] = ( 0,  1)
    S: tuple[int, int] = ( 0, -1)
    W: tuple[int, int] = (-1,  0)
    E: tuple[int, int] = ( 1,  0)


    def to_orientation(s:str):
        if s.upper() == "U" or s.upper() == "N":
            return Orientation.N
        if s.upper() == "D" or s.upper() == "S":
            return Orientation.S
        if s.upper() == "L" or s.upper() == "W":
            return Orientation.W
        if s.upper() == "R" or s.upper() == "E":
            return Orientation.E

        raise KeyError("ERROR : Illegal move string!")