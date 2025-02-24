from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.pupdevices import ColorSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait
import calibrations as cal

class Robot:
    def __init__(self, wheel_diameter=56, axle_track=80, turn_rate=45):
        # Initialise Motors (wheels)
        self.right_motor: Motor = Motor(Port.A)
        self.left_motor: Motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)

        # Initialise DriveBase
        self.drive_base: DriveBase = DriveBase(self.right_motor, self.left_motor,
                                               wheel_diameter=wheel_diameter, axle_track=axle_track
                                               )
        self.drive_base.settings(turn_rate=turn_rate)

        # Initialise PrimeHub
        self.prime_hub: PrimeHub = PrimeHub()
        self.prime_hub.speaker.volume(50)

        # Initialize & calibrate the sensors.
        self.left_sensor: ColorSensor = ColorSensor(Port.D)
        self.right_threshold = cal.calibrate_light_sensor(self, self.right_sensor)

        self.right_sensor: ColorSensor = ColorSensor(Port.E)
        self.left_threshold = cal.calibrate_light_sensor(self, self.left_sensor)

        # Calibrate acceleration:
        self.acceleration_error = cal.calibrate_acceleration(self)

        # Calibrate heading (direction robot is pointing)
        self.heading_threshold = cal.calibrate_heading(self)
    

    def navigate_maze(self):

        while not (self.is_tape_left() or self.is_tape_right()):
            self.left_motor.dc(30)
            self.right_motor.dc(30)
        
        if sum([self.is_tape_left(), self.is_tape_right()]):
            pass
    
    def is_tape_left(self): 
        return self.does_sensor_see_tape(self.left_sensor, self.left_threshold)
    
    def is_tape_right(self): 
        return  self.does_sensor_see_tape(self.right_sensor, self.right_threshold)

    def does_sensor_see_tape(self, sensor : ColorSensor, sensor_thresshold):
        return sensor.reflection() <= sensor_thresshold * 0.2

    
    def tell_me_what_you_see(self):
        self.left_motor.dc(30)
        self.right_motor.dc(30)

        while True:
            print("\nWhat I see:")
            print(f"Left sensor's Reflection = {self.left_sensor.reflection()}")
            print(f"Right sensor's Reflection = {self.right_sensor.reflection()}")
            wait(100) # Wait 1 seconds