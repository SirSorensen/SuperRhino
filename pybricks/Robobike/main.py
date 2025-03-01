from robot import Robot
from pybricks.tools import wait

robot = Robot()

robot.motor.run(300)

wait(2000)

robot.steering_wheel.run(100)
wait(600)
robot.steering_wheel.stop()

wait(2000)

robot.steering_wheel.run(-100)
wait(600)
robot.steering_wheel.stop()

wait(1500)