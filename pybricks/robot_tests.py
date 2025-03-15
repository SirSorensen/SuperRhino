from robot import Robot
from pybricks.tools import wait

def test_turn(robot : Robot):
    robot.legs.turn(360)

def test_eyes(robot : Robot):
    while True:
        print(robot.eyes.measure())

def test_forward(robot : Robot):
    robot.prime_hub.imu.reset_heading(180)
    start_heading = 180
    robot.legs.reset_distance()

    while True:
        robot.legs.go_forward()

        if abs(start_heading - robot.prime_hub.imu.heading()) > 10:
            robot.legs.hold()
            robot.legs.turn(start_heading - robot.prime_hub.imu.heading())

        stops = [57, 59, 63]
        stop_at_stops(robot, [stops[0]])
        stop_at_stops(robot, stops[:2])
        stop_at_stops(robot, stops)

def stop_at_stops(robot : Robot, stops):
    stop_distance = (sum(stops) * 10)
    if robot.legs.get_distance() <= stop_distance + 5 and robot.legs.get_distance() >= stop_distance - 5:
            print("STOPPING")
            print("Distance =", robot.legs.get_distance())
            robot.legs.hold()
            wait(1000)
            robot.legs.go_forward()
            wait(1000)