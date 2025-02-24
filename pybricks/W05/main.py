
from robot import Robot

print("\n\nTaking new light-reflection measurements:")
robot = Robot()

while True:
    robot.tell_me_what_you_see()