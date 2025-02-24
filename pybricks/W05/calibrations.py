from pybricks.parameters import Axis
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait


def calibrate_acceleration(robot) -> dict[str, float]:
    print(f"ready = {robot.prime_hub.imu.ready()}")
    print(f"stationary = {robot.prime_hub.imu.stationary()}")
    print(f"up = {robot.prime_hub.imu.up()}")
    print(f"tilt: pitch = {robot.prime_hub.imu.tilt()[0]}, roll = {robot.prime_hub.imu.tilt()[1]}")

    print()
    avg_acc_x_stationary = avg_measure(robot.prime_hub.imu.acceleration, parameters=Axis.X)
    print(f"acc_error(X) = {avg_acc_x_stationary} mm/s²")

    avg_acc_y_stationary = avg_measure(robot.prime_hub.imu.acceleration, parameters=Axis.Y)
    print(f"acc_error(Y) = {avg_acc_y_stationary} mm/s²")

    avg_acc_z_stationary = avg_measure(robot.prime_hub.imu.acceleration, parameters=Axis.Z)
    acceleration_error_z = 9815 - avg_acc_z_stationary
    print(f"acc_error(Z) = {acceleration_error_z} mm/s²")
    print()

    acceleration_error = {"X": avg_acc_x_stationary, "Y": avg_acc_y_stationary, "Z": acceleration_error_z}

    return acceleration_error


def calibrate_heading(robot) -> float:
    def turn_and_measure(deg, last_true):
        robot.drive_base.turn(deg)

        measure = avg_measure(robot.prime_hub.imu.heading)
        cur_deg = deg + last_true

        while abs(cur_deg) > 360:
            if cur_deg <= 0:
                cur_deg += 360
            else:
                cur_deg -= 360

        if (cur_deg == 0 and measure > 180) or (cur_deg < 0 and measure > 0):
            measure -= 360

    print("\n ### Calibrating heading:")
    headings = []
    headings.append(turn_and_measure(0, 0))
    headings.append(turn_and_measure(20, headings[-1][0]))
    headings.append(turn_and_measure(45, headings[-1][0]))
    headings.append(turn_and_measure(-65, headings[-1][0]))
    headings.append(turn_and_measure(-20, headings[-1][0]))
    headings.append(turn_and_measure(-45, headings[-1][0]))
    headings.append(turn_and_measure(65, headings[-1][0]))

    heading_errors = [abs(turn - deg) for (turn, deg) in headings]
    avg_heading_error = sum(heading_errors) / len(heading_errors)
    max_heading_error = max(heading_errors)
    # Midpoint between max and average error measured
    heading_threshold = (avg_heading_error + max_heading_error) / 2
    return heading_threshold


def calibrate_light_sensor(robot, sensor: ColorSensor) -> float:
    threshold = sensor.reflection()
    sensor.lights.on()
    wait(500)  # Wait 1.5 seconds
    print("threshold (lights on) =", threshold)
    return threshold * 0.9


def avg_measure(measurement_func, parameters=None, measure_num=100) -> float:
    measurements = []
    for _ in range(measure_num):
        if parameters is None:
            measurements.append(measurement_func())
        else:
            measurements.append(measurement_func(parameters))
    avg_measurement = sum(measurements) / len(measurements)
    return avg_measurement
