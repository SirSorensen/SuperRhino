

class State:
    def __init__(self):
        pass

class INROOM(State):
    def __init__(self, entity_id, room_id):
        self.entity_id = entity_id
        self.room_id = room_id
        super().__init__()

    def __eq__(self, other):
        if isinstance(other, INROOM):
            return self.entity_id == other.entity_id and self.room_id == other.room_id
        return False

class NEXTTO(State):
    def __init__(self, entity_id, door_id):
        self.entity_id = entity_id
        self.door_id = door_id
        super().__init__()

    def __eq__(self, other):
        if isinstance(other, NEXTTO):
            return self.entity_id == other.entity_id and self.door_id == other.door_id
        return False

class CONNECTS(State):
    def __init__(self, door_id, room1_id, room2_id):
        self.door_id = door_id
        self.room1_id = room1_id
        self.room2_id = room2_id
        super().__init__()

    def __eq__(self, other):
        if isinstance(other, CONNECTS):
            return self.door_id == other.door_id and self.room1_id == other.room1_id and self.room2_id == other.room2_id
        return False

class STATUS(State):
    def __init__(self, door_id, is_open):
        self.door_id = door_id
        self.is_open = is_open
        super().__init__()

    def __eq__(self, other):
        if isinstance(other, STATUS):
            return self.door_id == other.door_id and self.is_open == other.is_open
        return False