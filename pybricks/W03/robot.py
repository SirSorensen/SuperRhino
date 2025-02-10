from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Axis, Stop
from pybricks.pupdevices import ColorSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from statistic_util import *


class Robot:
    def __init__(self, wheel_diameter = 56, axle_track = 80, turn_rate = 45):
        self.right_motor : Motor = Motor(Port.A)
        self.left_motor : Motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
        self.drive_base : DriveBase = DriveBase(self.right_motor, self.left_motor, 
                               wheel_diameter=wheel_diameter, axle_track=axle_track
                            )
        self.drive_base.settings(turn_rate=turn_rate)
        
        # Initialize the sensor.
        self.color_sensor : ColorSensor = ColorSensor(Port.C)
        self.measure_color_reflections()

        # Initialise Hub
        self.prime_hub : PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)
        self.color_sensor.lights.off()

        

    def calibrate_acceleration(self):
        print(f"ready = {self.prime_hub.imu.ready()}")
        print(f"stationary = {self.prime_hub.imu.stationary()}")
        print(f"up = {self.prime_hub.imu.up()}")
        print(f"tilt: pitch = {self.prime_hub.imu.tilt()[0]}, roll = {self.prime_hub.imu.tilt()[1]}")

        print()
        avg_acc_x_stationary = avg_measure(self.prime_hub.imu.acceleration, parameters=Axis.X)
        print(f"acc_error(X) = {avg_acc_x_stationary} mm/s²")

        avg_acc_y_stationary = avg_measure(self.prime_hub.imu.acceleration, parameters=Axis.Y)
        print(f"acc_error(Y) = {avg_acc_y_stationary} mm/s²")

        avg_acc_z_stationary = avg_measure(self.prime_hub.imu.acceleration, parameters=Axis.Z)
        acceleration_error_z = 9815 - avg_acc_z_stationary
        print(f"acc_error(Z) = {acceleration_error_z} mm/s²")
        print()

        self.acceleration_error = {"X":avg_acc_x_stationary, "Y":avg_acc_y_stationary, "Z":acceleration_error_z}
    
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
        self.heading_threshold = (avg_heading_error + max_heading_error) / 2 #Midpoint between max and average error measured
        print(f"Heading-threshold = {self.heading_threshold}")

    def turn_and_measure(self, deg, last_true):
        self.drive_base.turn(deg)
        
        measure = avg_measure(self.prime_hub.imu.heading)
        cur_deg = deg + last_true

        while abs(cur_deg) > 360:
            if cur_deg <= 0:
                cur_deg += 360
            else:
                cur_deg -= 360

        if (cur_deg == 0 and measure > 180) or (cur_deg < 0 and measure > 0):
            measure -= 360

        return (cur_deg, measure)
        
    def drive_forward(self, distance : int):
        if distance < 20:
            raise Exception("Distance has to be at least 20!")

        start_heading = self.prime_hub.imu.heading()
        cur_distance = self.drive_base.distance()
        self.drive_base.straight(1000, then=Stop.COAST_SMART, wait=False)

        for _ in range(distance//10):
            current_heading = self.prime_hub.imu.heading()
            heading_dif = abs(current_heading - start_heading)
            if heading_dif > self.heading_threshold:
                print("Error!! I have turned!")
                self.drive_base.brake()
                if current_heading > start_heading:
                    print("Turning left")
                    self.drive_base.turn(-heading_dif)
                else:
                    print("Turning right")
                    self.drive_base.turn(heading_dif)
                self.drive_base.straight(((distance%10)*100) + cur_distance - self.drive_base.distance(), then=Stop.COAST_SMART, wait=False)
            else:
                print("Yay! Everything is fine!")
        
        self.drive_base.straight(1000, then=Stop.COAST_SMART, wait=False)

        self.drive_base.brake()
        print("Done!", self.drive_base.done())

    def measure_color_reflections(self):
        self.table_reflection = self.color_sensor.reflection()
        self.color_sensor.lights.on()
        wait(1500) # Wait 1.5 seconds
        print("self.table_reflection (lights on) =", self.table_reflection)


    def drive_straight_stop_at_edge(self):
        stop_watch = StopWatch()
        last_seen_was_light = True

        print("Let's go!")
        while True:
            self.left_motor.dc(30)
            self.right_motor.dc(30)
            cur_reflection = self.color_sensor.reflection()
            
            if cur_reflection < (self.table_reflection * 0.2):
                stop_watch.resume() # now we start timer
                print(f"I have seen darkness in {stop_watch.time()} ms (Current reflection = {cur_reflection} and that is < ({self.table_reflection} * 0.9))")

                if (stop_watch.time() >= 250):
                    print("Enough darkness!")
                    self.prime_hub.speaker.beep()
                    self.left_motor.brake()
                    self.right_motor.brake()
                    self.left_motor.dc(-30)
                    self.right_motor.dc(-30)
                    while cur_reflection < (self.table_reflection * 0.9):
                        cur_reflection = self.color_sensor.reflection()
                    self.left_motor.brake()
                    self.right_motor.brake()
                    # Turn
                    self.drive_base.turn(90)
            else:
                stop_watch.pause()
                stop_watch.reset()
    

                