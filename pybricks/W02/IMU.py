from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Axis, Stop
from pybricks.pupdevices import ColorSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait

def avg_measure(measurement_func, parameters=None, measure_num=100):
    measurements = []
    for _ in range(measure_num):
        if parameters is None:
            measurements.append(measurement_func())
        else:
            measurements.append(measurement_func(parameters))
    avg_measurement = sum(measurements)/len(measurements)
    return avg_measurement

# Initialize DriveBase
    # Param config
WHEEL_DIAMETER = 56
AXLE_TRACK = 80
TURN_RATE = 45
RIGHT_MOTOR = Motor(Port.A)
LEFT_MOTOR = Motor(Port.B, Direction.COUNTERCLOCKWISE)

drive_base = DriveBase(LEFT_MOTOR, RIGHT_MOTOR,
                       wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
drive_base.settings(turn_rate=TURN_RATE)


# Initialize the sensor.
color_sensor = ColorSensor(Port.C)
color_sensor.lights.off()


# Initialise Hub
prime_hub = PrimeHub()
print(f"ready = {prime_hub.imu.ready()}")
print(f"stationary = {prime_hub.imu.stationary()}")
print(f"up = {prime_hub.imu.up()}")
print(f"tilt: pitch = {prime_hub.imu.tilt()[0]}, roll = {prime_hub.imu.tilt()[1]}")

print()
avg_acc_x_stationary = avg_measure(prime_hub.imu.acceleration, parameters=Axis.X)
print(f"acc_error(X) = {avg_acc_x_stationary} mm/s²")

acc_y_tests = []
avg_acc_y_stationary = avg_measure(prime_hub.imu.acceleration, parameters=Axis.Y)
print(f"acc_error(Y) = {avg_acc_y_stationary} mm/s²")

avg_acc_z_stationary = avg_measure(prime_hub.imu.acceleration, parameters=Axis.Z)
acceleration_error_z = 9815 - avg_acc_z_stationary
print(f"acc_error(Z) = {acceleration_error_z} mm/s²")
print()




acc_error = {"X":avg_acc_x_stationary, "Y":avg_acc_y_stationary, "Z":acceleration_error_z}


print("\n ### Calibrating heading:")

headings = []

def turn_and_measure(deg):
    drive_base.turn(deg)
    
    if len(headings) == 0:
        last_true = 0
    else:
        last_true = headings[-1][0]
    
    measure = avg_measure(prime_hub.imu.heading)
    cur_deg = deg + last_true

    while abs(cur_deg) > 360:
        if cur_deg <= 0:
            cur_deg += 360
        else:
            cur_deg -= 360

    if (cur_deg == 0 and measure > 180) or (cur_deg < 0 and measure > 0):
        measure -= 360
    


    return (cur_deg, measure)

headings.append(turn_and_measure(0))
headings.append(turn_and_measure(20))
headings.append(turn_and_measure(45))
headings.append(turn_and_measure(-65))
headings.append(turn_and_measure(-20))
headings.append(turn_and_measure(-45))
headings.append(turn_and_measure(65))
    
def print_headings():
    for (turn, deg) in headings:
        print("True degrees", turn)
        print("Measured degrees", deg)
        print("Error", abs(turn-deg))
        if turn != 0:
            print("Error-percentage ", ((turn-deg)/(turn))*100, "%", sep="")
        print()

heading_errors = [abs(turn-deg) for (turn, deg) in headings]
avg_heading_error = sum(heading_errors)/len(heading_errors)
max_heading_error = max(heading_errors)
threshold = (avg_heading_error + max_heading_error) / 2 #Midpoint between max and average error measured
print(f"threshold = {threshold}")



start_heading = prime_hub.imu.heading()
cur_distance = drive_base.distance()
drive_base.straight(1000, then=Stop.COAST_SMART, wait=False)

for _ in range(10):
    current_heading = prime_hub.imu.heading()
    heading_dif = abs(current_heading - start_heading)
    if heading_dif > threshold:
        print("Error!! I have turned!")
        drive_base.brake()
        if current_heading > start_heading:
            print("Turning left")
            drive_base.turn(-heading_dif)
        else:
            print("Turning right")
            drive_base.turn(heading_dif)
        drive_base.straight(1000 + cur_distance - drive_base.distance(), then=Stop.COAST_SMART, wait=False)
    else:
        print("Yay! Everything is fine!")

drive_base.brake()
print("Done!", drive_base.done())
