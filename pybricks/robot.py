from robot_eyes import RobotEyes
from robot_legs import RobotLegs
from pybricks.parameters import Port
from pybricks.hubs import PrimeHub
from pybricks.tools import wait


class Robot:
    def __init__(self):
        ### Measurements ###
        # About 8 cm from eye to leg

        # Initialise Motors (wheels)
        self.legs : RobotLegs = RobotLegs(Port.A, Port.E)

        # Initialize & calibrate the sensors
        self.eyes : RobotEyes = RobotEyes(Port.B, Port.F)

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)

    def test_turn(self):
        self.legs.turn(360)

    def test_eyes(self):
        while True:
            print(self.eyes.measure())

    def test_forward(self):
        self.prime_hub.imu.reset_heading(180)
        start_heading = 180
        self.legs.reset_distance()

        while True:
            self.legs.go_forward()

            if abs(start_heading - self.prime_hub.imu.heading()) > 10:
                self.legs.hold()
                self.legs.turn(start_heading - self.prime_hub.imu.heading())
            if self.eyes.do_I_see_a_cliff():
                print("I see a cliff!")
                self.legs.hold()
                self.legs.go_back()
                wait(1000)
                self.legs.turn(90)
                self.prime_hub.imu.reset_heading(180)



            stops = [57, 59, 63]
            self.stop_at_stops([stops[0]])
            self.stop_at_stops(stops[:2])
            self.stop_at_stops(stops)

    def stop_at_stops(self, stops):
        stop_distance = (sum(stops) * 10)
        if self.legs.get_distance() <= stop_distance + 5 and self.legs.get_distance() >= stop_distance - 5:
                print("STOPPING")
                print("Distance =", self.legs.get_distance())
                self.legs.hold()
                wait(1000)
                self.legs.go_forward()
                wait(1000)

