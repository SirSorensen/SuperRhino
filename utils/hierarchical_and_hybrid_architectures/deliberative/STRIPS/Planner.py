import State as st

class Planner:
    def __init__(self, cur_states : list[st.State], goal_state : st.State):
        self.cur_states = cur_states
        self.goal_state = goal_state

    def difference(self):
        if self.goal_state in self.cur_states:
            return True
        return False
