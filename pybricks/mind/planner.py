from utils.queue import list_to_queue, Queue
from utils.cardinal_direction import CardinalDirection


class Planner:
    def __init__(self, solution_str: str):
        print("Solution:", solution_str)
        solution_list = [CardinalDirection.to_cardinal_direction(s) for s in solution_str]  # From string to orientations
        self.solution: Queue = list_to_queue(solution_list)

    def next_move(self) -> CardinalDirection | None:
        return self.solution.dequeue()

    def is_done(self) -> bool:
        return self.solution.is_empty()
