
import State as st

class Operator:
    def __init__(self):
        pass

    def preconditions(self) -> bool:
        return True

    def add_list(self) -> list[st.State]:
        return []

    def delete_list(self) -> list[st.State]:
        return []



class GOTODOOR(Operator):
    # GOTODOOR(IT, dx)
    def __init__(self, entity_id, door_id):
        self.entity_id = entity_id
        self.door_id = door_id
        super().__init__()

    def preconditions(self, states : list[st.State]) -> bool:
        # INROOM(IT, rk)
        in_rooms = list(filter(
                                lambda state: type(state) is st.INROOM and state.entity_id == self.entity_id,
                                states
                              ))

        if len(in_rooms) == 0:
            return False

        room_id = in_rooms[0].room_id


        # CONNECTS(dx, rk, rm)
        connects = list(filter(
                                lambda state: type(state) is st.CONNECTS and state.door_id == self.door_id and (state.room1_id == room_id or state.room2_id == room_id),
                                states
                              ))
        if len(connects) == 0:
            return False

        return True

    def add_list(self) -> list[st.State]:
        # NEXTO(IT, dx)
        return [st.NEXTTO(self.entity_id, self.door_id)]



class GOTHRUDOOR(Operator):
    # GOTHRUDOOR(IT, dx)
    def __init__(self, entity_id, door_id):
        self.entity_id = entity_id
        self.door_id = door_id

        self.cur_room = None
        self.next_room = None
        super().__init__()

    def preconditions(self, states : list[st.State]) -> bool:

        # NEXTO(IT, dx)
        next_tos = list(filter(
                                lambda state: type(state) is st.NEXTTO and state.entity_id == self.entity_id and state.door_id == self.door_id,
                                states
                              ))

        if len(next_tos) == 0:
            return False


        # INROOM(IT, rk)
        in_rooms = list(filter(
                                lambda state: type(state) is st.INROOM and state.entity_id == self.entity_id,
                                states
                              ))

        if len(in_rooms) == 0:
            return False
        self.cur_room = in_rooms[0].room_id

        # CONNECTS(dx, rk, rm)
        connects = list(filter(
                                lambda state: type(state) is st.CONNECTS and state.door_id == self.door_id and (state.room1_id == self.cur_room or state.room2_id == self.cur_room),
                                states
                              ))

        if len(connects) == 0:
            return False

        if connects[0].room1_id == self.cur_room:
            self.next_room = connects[0].room2_id
        else:
            self.next_room = connects[0].room1_id

        # STATUS(dx, OPEN)
        statuses = list(filter(
                                lambda state: type(state) is st.STATUS and state.door_id == self.door_id and state.is_open,
                                states
                              ))

        if len(statuses) == 0:
            return False


        return True



    def add_list(self) -> list[st.State]:
        # INROOM(IT, rm)
        return [st.INROOM(self.entity_id, self.next_room)]

    def delete_list(self) -> list[st.State]:
        # INROOM(IT, rk)
        return [st.INROOM(self.entity_id, self.cur_room)]
