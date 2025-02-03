from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Axis
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

# Initialize DriveBase
DRIVE_BASE = DriveBase(LEFT_MOTOR, RIGHT_MOTOR,
                       wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
DRIVE_BASE.settings(turn_rate=TURN_RATE)


# Initialise Hub
hub = PrimeHub()
print(f"ready = {hub.imu.ready()}")
print(f"stationary = {hub.imu.stationary()}")
print(f"up = {hub.imu.up()}")
print(f"tilt: pitch = {hub.imu.tilt()[0]}, roll = {hub.imu.tilt()[1]}")

print()
avg_acc_x_stationary = sum([hub.imu.acceleration(Axis.X) for _ in range(100)]) / 100
print(f"acceleration(X) = {avg_acc_x_stationary} mm/s²")
print(f"error(X) = {avg_acc_x_stationary} mm/s²")
print(f"true acceleration(X) = {0.0} mm/s²")
print(f"true(er) acceleration(X) = {hub.imu.acceleration(Axis.X) - avg_acc_x_stationary} mm/s²")
print()

acc_y_tests = []
avg_acc_y_stationary = sum([hub.imu.acceleration(Axis.Y) for _ in range(100)]) / 100
print(f"acceleration(Y) = {avg_acc_y_stationary} mm/s²")
print(f"error(Y) = {avg_acc_y_stationary} mm/s²")
print(f"true acceleration(Y) = {0.0} mm/s²")
print(f"true(er) acceleration(Y) = {hub.imu.acceleration(Axis.Y) - avg_acc_y_stationary} mm/s²")

print()

avg_acc_z_stationary = sum([hub.imu.acceleration(Axis.Z) for _ in range(100)]) / 100
print(f"acceleration(Z) = {avg_acc_z_stationary} mm/s²")
acceleration_error_z = 9815 - avg_acc_z_stationary
print(f"error(Z) = {acceleration_error_z} mm/s²")
print(f"true acceleration(Z) = {avg_acc_z_stationary - acceleration_error_z} mm/s²")
print(f"true(er) acceleration(Z) = {hub.imu.acceleration(Axis.Z) - acceleration_error_z} mm/s²")
print()
print(f"angular_velocity(X) = {hub.imu.angular_velocity(Axis.X)} deg/s")
print(f"angular_velocity(Y) = {hub.imu.angular_velocity(Axis.Y)} deg/s")
print(f"angular_velocity(Z) = {hub.imu.angular_velocity(Axis.Z)} deg/s")



acc_error = {"X":avg_acc_x_stationary, "Y":avg_acc_y_stationary, "Z":acceleration_error_z}


print()
print(" ### Calibrating heading:")


headings = [(0.00000000001, hub.imu.heading())]

DRIVE_BASE.turn(90)
headings.append((90, hub.imu.heading()))

DRIVE_BASE.turn(90)
headings.append((180, hub.imu.heading()))

DRIVE_BASE.turn(90)
headings.append((270, hub.imu.heading()))

DRIVE_BASE.turn(90)
headings.append((360, hub.imu.heading()))

printable_result = [(turn, deg, turn-deg, str(((turn-deg)/(turn))*100) + " %") for (turn, deg) in headings]

for r in printable_result:
    print("True degrees " + str(r[0]))
    print("Measured degrees " + str(r[1]))
    print("Error " + str(r[2]))
    print("Error-percentage " + str(r[3]))
    print()

avg_heading_error = sum([abs(turn-deg) for (turn, deg) in headings])/len(headings)



start_heading = hub.imu.heading()

for _ in range(10):
    current_heading = hub.imu.heading()
    if abs(current_heading - start_heading) > avg_heading_error:
        if start_heading > current_heading:
            DRIVE_BASE.turn(start_heading - current_heading)
        else:
            DRIVE_BASE.turn(current_heading - start_heading)
    
    DRIVE_BASE.straight(100)



