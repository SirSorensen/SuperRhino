from robot import Robot
from pybricks.tools import wait

speed = 500
robot = Robot()


robot.left_motor.run(speed)
robot.right_motor.run(speed)

wait(3000)


robot.left_motor.run(speed)
robot.right_motor.run(speed*0.6)

wait(3000)

robot.left_motor.run(speed)
robot.right_motor.run(speed)

wait(3000)

robot.left_motor.hold()
robot.right_motor.hold()
