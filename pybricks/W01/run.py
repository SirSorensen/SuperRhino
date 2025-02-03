from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.pupdevices import ColorSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Initialize the sensor.
sensor = ColorSensor(Port.C)
sensor.lights.off()

# Initialize a motor on port A.
# Wheel diamater = 5.5 cm
# Wheel circumfrance = ca. 17,27
right_motor = Motor(Port.A)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)

# Initialize the drive base. In this example, the wheel diameter is 56mm.
# The distance between the two wheel-ground contact points is 112mm.
drive_base = DriveBase(left_motor, right_motor,
                       wheel_diameter=56, axle_track=80)
drive_base.settings(turn_rate=20)

drive_base.turn(20)


# drive_base.straight(900)

# turn left testing

# drive_base.straight(450)

# The robot starts on the floor and
# can be commanded to move forward 90cm and
# left 45cm and point at an angle relatively
# to the starting direction of 30 degrees
