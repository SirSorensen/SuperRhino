from numpy import cos, sin, pi
import random

from sensor import SingleRayDistanceAndColorSensor


class DifferentialDriveRobot:
    def __init__(
        self,
        env,
        x,
        y,
        theta,
        axel_length=40,
        wheel_radius=10,
        max_motor_speed=2 * pi,
        kinematic_timestep=0.01,
    ):
        self.env = env
        self.x = x
        self.y = y
        self.theta = theta  # Orientation in radians
        self.axel_length = axel_length  # in cm
        self.wheel_radius = wheel_radius  # in cm

        self.kinematic_timestep = kinematic_timestep

        self.collided = False
        self.max_motor_speed = 1.5

        # Motor speeds (rad/s)
        self.left_motor_speed = 0
        self.right_motor_speed = 0
        # Initialize multiple distance sensors (rays) to cover 180 degrees
        # Angles relative to robot heading: -45°, 0°, +45°
        max_dist = 100  # max sensing distance in cm
        self.sensors = [
            SingleRayDistanceAndColorSensor(max_dist, -pi / 4),
            SingleRayDistanceAndColorSensor(max_dist, 0.0),  # front sensor
            SingleRayDistanceAndColorSensor(max_dist, pi / 4),
        ]
        # Controller state for wall-search and wall-follow behaviors
        self.searching_wall = True
        # Distance within which a wall is considered detected (cm)
        self.detection_range = 50.0
        # Target distance to maintain from wall during wall-following (cm)
        self.wall_follow_target = 30.0
        # Proportional gain for wall-following control
        self.wall_follow_kp = 0.05
        # Safety distance to maintain frontally to avoid collisions (cm)
        self.front_safety_distance = 30.0

    def move(self, robot_timestep):  # run the control algorithm here
        # update sensors at current pose
        self.sense()

        # Wall-search and wall-follow control
        # Read sensor distances (default to inf if no reading)
        dists = []
        for s in self.sensors:
            d = s.latest_reading[0] if s.latest_reading else float("inf")
            dists.append(d)

        # Wall-search and wall-follow control
        # If still searching and no wall detected, perform search behavior
        if self.searching_wall and min(dists) > self.detection_range:
            self.left_motor_speed = 0.5 * self.max_motor_speed
            self.right_motor_speed = self.max_motor_speed
        else:
            # Switch to wall-follow mode
            self.searching_wall = False
            # Base forward speed for wall-follow
            base_speed = 0.5 * self.max_motor_speed
            # Frontal safety check: use front sensor (index 1)
            front_dist = dists[1]
            if front_dist < self.front_safety_distance:
                # Pivot away from wall to avoid head-on collision (pivot in place)
                self.left_motor_speed = base_speed
                self.right_motor_speed = -base_speed
            else:
                # Lateral wall-follow control using left-side sensor (index 0)
                left_dist = dists[0]
                error = left_dist - self.wall_follow_target
                adjust = self.wall_follow_kp * error
                # Compute wheel speeds with proportional control
                left_speed = base_speed - adjust
                right_speed = base_speed + adjust
                max_m = self.max_motor_speed
                # Ensure forward motion: clip speeds to [0, max_m]
                self.left_motor_speed = max(min(left_speed, max_m), 0.0)
                self.right_motor_speed = max(min(right_speed, max_m), 0.0)

        # simulate kinematics during one execution cycle of the robot
        self._step_kinematics(robot_timestep)

        # check for collision (collision should be avoided by control)
        self.collided = self.env.check_collision(
            self.get_robot_pose(), self.get_robot_radius()
        )

    def _step_kinematics(self, robot_timestep):
        for _ in range(
            int(robot_timestep / self.kinematic_timestep)
        ):  # the kinematic model is updated in every step for robot_timestep/self.kinematic_timestep times
            # odometry is used to calculate where we approximately end up after each step
            pos = self._odometer(self.kinematic_timestep)
            self.x = pos.x
            self.y = pos.y
            self.theta = pos.theta
            # Add a small amount of noise to the orientation and/or position
            # noise = random.gauss(0, self.theta_noise_level)
            # self.theta += noise

    def sense(self):
        # update all sensors with current obstacles and pose
        obstacles = self.env.get_obstacles()
        robot_pose = self.get_robot_pose()
        for s in self.sensors:
            s.generate_beam_and_measure(robot_pose, obstacles)

    # this is in fact what a robot can predict about its own future position
    def _odometer(self, delta_time):
        left_angular_velocity = self.left_motor_speed
        right_angular_velocity = self.right_motor_speed

        v_x = cos(self.theta) * (
            self.wheel_radius * (left_angular_velocity + right_angular_velocity) / 2
        )
        v_y = sin(self.theta) * (
            self.wheel_radius * (left_angular_velocity + right_angular_velocity) / 2
        )
        omega = (
            self.wheel_radius * (left_angular_velocity - right_angular_velocity)
        ) / self.axel_length

        next_x = self.x + (v_x * delta_time)
        next_y = self.y + (v_y * delta_time)
        next_theta = self.theta + (omega * delta_time)

        # Ensure the orientation stays within the range [0, 2*pi)
        next_theta = next_theta % (2 * pi)

        return RobotPose(next_x, next_y, next_theta)

    def get_robot_pose(self):
        return RobotPose(self.x, self.y, self.theta)

    def get_robot_radius(self):
        return self.axel_length / 2

    def draw(self, surface):
        import pygame
        pygame.draw.circle(
            surface,
            (0, 255, 0),
            center=(self.x, self.y),
            radius=self.axel_length / 2,
            width=1,
        )

        # Calculate the left and right wheel positions
        half_axl = self.axel_length / 2
        left_wheel_x = self.x - half_axl * sin(self.theta)
        left_wheel_y = self.y + half_axl * cos(self.theta)
        right_wheel_x = self.x + half_axl * sin(self.theta)
        right_wheel_y = self.y - half_axl * cos(self.theta)

        # Calculate the heading line end point
        heading_length = half_axl + 2
        heading_x = self.x + heading_length * cos(self.theta)
        heading_y = self.y + heading_length * sin(self.theta)

        # Draw the axle line
        pygame.draw.line(
            surface,
            (0, 255, 0),
            (left_wheel_x, left_wheel_y),
            (right_wheel_x, right_wheel_y),
            3,
        )

        # Draw the heading line
        pygame.draw.line(
            surface, (255, 0, 0), (self.x, self.y), (heading_x, heading_y), 5
        )

        # Draw sensor beams
        for s in self.sensors:
            s.draw(self.get_robot_pose(), surface)


class RobotPose:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    # this is for pretty printing
    def __repr__(self) -> str:
        return f"x:{self.x},y:{self.y},theta:{self.theta}"
