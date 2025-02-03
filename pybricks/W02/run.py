from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.pupdevices import ColorSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait


# Error
TURN_ERROR = 0.1

# Param config
WHEEL_DIAMETER = 56
AXLE_TRACK = 80
TURN_RATE = 45
TURN_ACCELERATION = 20
RIGHT_MOTOR = Motor(Port.A)
LEFT_MOTOR = Motor(Port.B, Direction.COUNTERCLOCKWISE)
COLOR_SENSOR = ColorSensor(Port.C)

# Initialize the sensor.
COLOR_SENSOR.lights.off()
DRIVE_BASE = DriveBase(LEFT_MOTOR, RIGHT_MOTOR,
                       wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
DRIVE_BASE.settings(turn_rate=TURN_RATE)


# POINT A
# DRIVE_BASE.straight(975)
# DRIVE_BASE.turn(90+(TURN_ERROR*90))
# DRIVE_BASE.straight(185)
# DRIVE_BASE.turn(120+(TURN_ERROR*120))
# DRIVE_BASE.straight(-75)


# POINT B
DRIVE_BASE.straight(1500)
DRIVE_BASE.turn(-85+(TURN_ERROR*-85))
DRIVE_BASE.straight(10)

# POINT C
# DRIVE_BASE.straight(1300)
# DRIVE_BASE.turn(-85+(TURN_ERROR*-85))
# DRIVE_BASE.straight(270)
# DRIVE_BASE.turn(40+(TURN_ERROR*40))
