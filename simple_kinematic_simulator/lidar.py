import pygame
import math

from sensor import SingleRayDistanceAndColorSensor
from robot_pose import RobotPose


beam_range = range(0, 360, 45)


class Lidar:
    def __init__(self, max_distance_cm = 8):
        self.sensors : dict[int, SingleRayDistanceAndColorSensor] = dict()
        for degree in beam_range:
            rad = math.radians(degree)
            s = SingleRayDistanceAndColorSensor(max_distance_cm, rad)
            self.sensors[degree] = s


    def generate_beam_and_measure(self, robot_pose, obstacles):
        for degree in beam_range:
            self.sensors[degree].generate_beam_and_measure(robot_pose, obstacles)

    def draw(self, robot_pose : RobotPose, surface : pygame.Surface):
        for degree in beam_range:
            self.sensors[degree].draw(robot_pose, surface)





