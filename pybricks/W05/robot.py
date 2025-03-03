import calibrations as cal
import urandom

from pybricks.hubs import PrimeHub
from pybricks.parameters import Port
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.tools import StopWatch, wait


class Robot:
    def __init__(self):
        # Initialise Motors (wheels)
        self.left_motor: Motor = Motor(Port.A)
        self.right_motor: Motor = Motor(Port.E)

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)

        # Initialize & calibrate the sensors.
        self.left_sensor: ColorSensor = ColorSensor(Port.B)
        self.left_threshold = cal.calibrate_light_sensor(self, self.left_sensor)

        self.right_sensor: ColorSensor = ColorSensor(Port.F)
        self.right_threshold = cal.calibrate_light_sensor(self, self.right_sensor)

        # Calibrate acceleration:
        self.acceleration_error = cal.calibrate_acceleration(self)

        # Calibrate heading (direction robot is pointing)
        self.heading_threshold = cal.calibrate_heading(self)

    def navigate_maze(self):
        while True:
            print("Heading =", self.prime_hub.imu.heading())
            self.go_straight()

            if self.is_tape_left() or self.is_tape_right():
                path_left = False
                path_right = False
                while self.is_tape_left() or self.is_tape_right():
                    path_left = self.is_tape_left()
                    path_right = self.is_tape_right()
                wait(350)
                self.brake()

                if path_left and path_right:
                    choice = urandom.choice(["l", "r"])
                elif path_left:
                    choice = "l"
                else:
                    choice = "r"

                if choice == "l":
                    self.turn(90)
                else:
                    self.turn(-90)

    def time_me(self):
        stop_watch = StopWatch()
        stop_watch.reset()
        stop_watch.resume()  # now we start timer
        while self.is_tape_left() or self.is_tape_right():
            print(f"    Timer is at {stop_watch.time()}")
        print(f"Robot stopped at {stop_watch.time()}!")
        self.brake()
        stop_watch.pause()

    def go_straight(self):
        self.left_motor.dc(30)

    def brake(self):
        self.left_motor.brake()

    # figure out which paths are valid
    def turn_around_detect(self) -> tuple[bool, bool, bool, bool]:  # (left, right, forward, backward)
        self.left_motor.dc(30)
        while self.is_tape_left() or self.is_tape_right():
            pass

        self.left_motor.brake()
        self.turn(90)

    # turn in a (random) given valid direction
    def turn_direction(self, valid_directions: tuple[bool, bool, bool, bool]):
        pass

    def turn(self, angle):
        self.left_motor.brake()

        self.prime_hub.imu.reset_heading(180)
        start_heading = 180

        if angle > 0:
            self.right_motor.run_angle(5, 30)
        else:
            self.right_motor.run_angle(5, -30)

        self.left_motor.run(30)

        while abs(self.prime_hub.imu.heading() - start_heading) < abs(angle):
            print("Heading =", self.prime_hub.imu.heading())
            pass

        self.left_motor.brake()
        self.right_motor.run_angle(5, 0)

    def is_tape_left(self):
        return self.does_sensor_see_tape(self.left_sensor, self.left_threshold)

    def is_tape_right(self):
        return self.does_sensor_see_tape(self.right_sensor, self.right_threshold)

    def does_sensor_see_tape(self, sensor: ColorSensor, sensor_thresshold):
        return sensor.reflection() <= sensor_thresshold * 0.75

    def tell_me_what_you_see(self):
        self.left_motor.dc(30)

        while True:
            print("\nWhat I see:")
            print(f"Left sensor's Reflection = {self.left_sensor.reflection()}")
            print(f"Right sensor's Reflection = {self.right_sensor.reflection()}")
            wait(100)  # Wait 1 seconds
