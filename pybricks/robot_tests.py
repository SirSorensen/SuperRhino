from robot import Robot


def sokoban_test():
    r = Robot()
    r.sokoban_prep("UURRDRDDLRULULULDD", (0, 1))
    r.sokoban_run()