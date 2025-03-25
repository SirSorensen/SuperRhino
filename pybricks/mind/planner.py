from mind.utils.queue import list_to_queue, Queue
from mind.utils.orientation import Orientation


class Planner:
    def __init__(self, solution_str : str):
        print("Solution:", solution_str)
        solution_list = [Orientation.to_orientation(s) for s in solution_str] # From string to orientations
        self.solution : Queue = list_to_queue(solution_list)

    def next_move(self) -> Orientation|None:
        return self.solution.dequeue()

    def is_done(self) -> bool:
        return self.solution.is_empty()