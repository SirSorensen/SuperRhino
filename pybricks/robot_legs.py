
import calibrations as cal
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub


class RobotLegs:
    def __init__(self, left_port : Port, right_port : Port):
        # Initialise Motors (wheels)
        self.left_motor: Motor = Motor(left_port, Direction.COUNTERCLOCKWISE)
        self.right_motor: Motor = Motor(right_port)

        self.drive_base: DriveBase = DriveBase(self.left_motor, self.right_motor,
                                               wheel_diameter=56, axle_track=160
                                               )

        self.turn_rate = 50
        self.turn_degree = 40
        self.speed = 200

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)

        # Calibrate acceleration:
        self.acceleration_error = cal.calibrate_acceleration(self)

    def go_forward(self):
        self.left_motor.run(self.speed)
        self.right_motor.run(self.speed)


        start_heading = self.prime_hub.imu.reset_heading(180)

        while abs(start_heading - self.prime_hub.imu.heading()) > 10:
            self.hold()
            self.turn(start_heading - self.prime_hub.imu.heading())

        self.go_forward()



    def go_back(self):
        pass  # TODO

    def hold(self):
        self.left_motor.hold()
        self.right_motor.hold()

    def turn(self, angle):
        self.drive_base.turn(angle)