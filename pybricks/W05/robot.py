from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Axis
from pybricks.pupdevices import ColorSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait


class Robot:
    def __init__(self, wheel_diameter=56, axle_track=80, turn_rate=45):
        self.right_motor: Motor = Motor(Port.A)
        self.left_motor: Motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
        self.drive_base: DriveBase = DriveBase(self.right_motor, self.left_motor,
                                               wheel_diameter=wheel_diameter, axle_track=axle_track
                                               )
        self.drive_base.settings(turn_rate=turn_rate)

        # Initialize the sensor.
        self.horizontal_sensor: ColorSensor = ColorSensor(Port.C)
        self.horizontal_threshold = self.calibrate_light_sensor(
            self.horizontal_sensor)

        self.vertical_sensor: ColorSensor = ColorSensor(Port.D)
        self.vertical_threshold = self.calibrate_light_sensor(
            self.vertical_sensor)

        # Initialise Hub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)
        self.horizontal_sensor.lights.off()

    def calibrate_acceleration(self):
        print(f"ready = {self.prime_hub.imu.ready()}")
        print(f"stationary = {self.prime_hub.imu.stationary()}")
        print(f"up = {self.prime_hub.imu.up()}")
        print(f"tilt: pitch = {self.prime_hub.imu.tilt()[
              0]}, roll = {self.prime_hub.imu.tilt()[1]}")

        print()
        avg_acc_x_stationary = avg_measure(
            self.prime_hub.imu.acceleration, parameters=Axis.X)
        print(f"acc_error(X) = {avg_acc_x_stationary} mm/s²")

        avg_acc_y_stationary = avg_measure(
            self.prime_hub.imu.acceleration, parameters=Axis.Y)
        print(f"acc_error(Y) = {avg_acc_y_stationary} mm/s²")

        avg_acc_z_stationary = avg_measure(
            self.prime_hub.imu.acceleration, parameters=Axis.Z)
        acceleration_error_z = 9815 - avg_acc_z_stationary
        print(f"acc_error(Z) = {acceleration_error_z} mm/s²")
        print()

        self.acceleration_error = {"X": avg_acc_x_stationary,
                                   "Y": avg_acc_y_stationary, "Z": acceleration_error_z}

    def calibrate_heading(self):
        print("\n ### Calibrating heading:")
        headings = []
        headings.append(self.turn_and_measure(0, 0))
        headings.append(self.turn_and_measure(20, headings[-1][0]))
        headings.append(self.turn_and_measure(45, headings[-1][0]))
        headings.append(self.turn_and_measure(-65, headings[-1][0]))
        headings.append(self.turn_and_measure(-20, headings[-1][0]))
        headings.append(self.turn_and_measure(-45, headings[-1][0]))
        headings.append(self.turn_and_measure(65, headings[-1][0]))

        heading_errors = [abs(turn-deg) for (turn, deg) in headings]
        avg_heading_error = sum(heading_errors)/len(heading_errors)
        max_heading_error = max(heading_errors)
        # Midpoint between max and average error measured
        self.heading_threshold = (avg_heading_error + max_heading_error) / 2
        print(f"Heading-threshold = {self.heading_threshold}")

    def calibrate_light_sensor(self, sensor: ColorSensor):
        threshold = sensor.reflection()
        self.horizontal_sensor.lights.on()
        wait(500)  # Wait 1.5 seconds
        print("threshold (lights on) =", threshold)
        return threshold

    def tell_me_what_you_see(self):
        print("\nWhat I see:")
        print(f"Vertical sensor's Reflection = {self.vertical_sensor.reflection()}")
        print(f"Vertical sensor's Ambient = {self.vertical_sensor.ambient()}")
        print(f"Vertical sensor's Color = {self.vertical_sensor.color()}")
        print(f"Vertical sensor's Detectable Colors = {self.vertical_sensor.detectable_colors()}")
        print(f"Vertical sensor's HSV = {self.vertical_sensor.hsv()}")
        wait(500) # Wait 5 seconds
