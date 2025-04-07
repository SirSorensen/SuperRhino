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

    def get_smallest_distance(self):
        cur_min = None
        min_angle = 0
        for degree in beam_range:
            (distance, color, intersect_point) = self.sensors[degree].latest_reading
            if cur_min is None or distance < cur_min:
                cur_min = distance
                min_angle = degree

        return (cur_min, min_angle)


    def draw(self, robot_pose : RobotPose, surface : pygame.Surface):
        for _, sensor in self.sensors.items():
            sensor.draw(robot_pose, surface)





