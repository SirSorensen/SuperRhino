from mind.utils.queue import list_to_queue, Queue


class Planner:
    def __init__(self, solution_str : str):
        print("Solution:", solution_str)
        self.solution : Queue = list_to_queue(solution_str)


    def next_move(self) -> str|None:
        return self.solution.dequeue()

    def is_done(self) -> bool:
        return self.solution.is_empty()