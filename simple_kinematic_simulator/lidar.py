import pygame
import math

from sensor import SingleRayDistanceAndColorSensor
from robot_pose import RobotPose


beam_range = range(15, 360, 30)


class Lidar:
    def __init__(self, max_distance_cm = 8):
        self.sensors : dict[int, SingleRayDistanceAndColorSensor] = dict()
        self.sensors[0] = SingleRayDistanceAndColorSensor(max_distance_cm, 0)
        for degree in beam_range:
            rad = math.radians(degree)
            s = SingleRayDistanceAndColorSensor(max_distance_cm, rad)
            self.sensors[degree] = s


    def generate_beam_and_measure(self, robot_pose, obstacles):
        for _, sensor in self.sensors.items():
            sensor.generate_beam_and_measure(robot_pose, obstacles)

    def draw(self, robot_pose : RobotPose, surface : pygame.Surface):
        for _, sensor in self.sensors.items():
            sensor.draw(robot_pose, surface)





