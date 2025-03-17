from labyrinth import Labyrinth
from our_queue import list_to_queue, Queue


class Planner:
    def __init__(self):
        pass

    def plan(self, sokoban_map : str):
        lab = Labyrinth()
        grid = lab.parse_sokoban_map(sokoban_map)
        solution_str : str = lab.sokoban_solver(grid)
        self.solution : Queue = list_to_queue(solution_str)

    def next_move(self) -> str|None:
        return self.solution.dequeue()

    def is_done(self) -> bool:
        return self.solution.is_empty()
