from physiology.movement import Movement
from pybricks.parameters import Port
from pybricks.hubs import PrimeHub


class Robot:
    def __init__(self):

        # Initialise Motors (wheels)
        self.legs: Movement = Movement(Port.B, Port.A)

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)


