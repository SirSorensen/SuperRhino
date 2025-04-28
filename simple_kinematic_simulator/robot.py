import pygame
from environment import Environment
from numpy import cos, pi, sin
from robot_pose import RobotPose
from sensor import SingleRayDistanceAndColorSensor


class DifferentialDriveRobot:
    def __init__(self, env : Environment, x : float, y : float, theta : float, axel_length=40, wheel_radius=10, max_motor_speed=2*pi, kinematic_timestep=0.01):
        self.env : Environment = env
        self.x : float = x
        self.y : float = y
        self.theta : float = theta  # Orientation in radians
        self.axel_length = axel_length # in cm
        self.wheel_radius = wheel_radius # in cm
        self.kinematic_timestep : float = kinematic_timestep
        # tuples consist of (width, height) and represent squares
        # self.floor_plan = [[0]*env.width for _ in range(env.height)]
        self.floor_plan = [[0 for _ in range(env.width)] for _ in range(env.height)]
        self.collided : bool = False

        self.left_motor_speed  = 3 #rad/s
        self.right_motor_speed = 1 #rad/s
        self.theta_noise_level = 0.01
        self.max_sensor_distance = 100
        self.sensor : SingleRayDistanceAndColorSensor = SingleRayDistanceAndColorSensor(self.max_sensor_distance, 0)


    def move(self, robot_timestep : float): # run the control algorithm here
        # simulate kinematics during one execution cycle of the robot
        self._step_kinematics(robot_timestep)

        # check for collision
        self.collided = self.env.check_collision(self.get_robot_pose(), self.get_robot_radius())

        # update sensors
        self.sense()

        # run the control algorithm and update motor speeds
        # ...



    def _step_kinematics(self, robot_timestep : float):
        for _ in range(int(robot_timestep / self.kinematic_timestep)): # the kinematic model is updated in every step for robot_timestep/self.kinematic_timestep times
            # odometry is used to calculate where we approximately end up after each step
            pos = self._odometer(self.kinematic_timestep)
            self.x = pos.x
            self.y = pos.y
            self.theta = pos.theta
            # After approximating position we can update our internal map

            # Add a small amount of noise to the orientation and/or position
            # noise = random.gauss(0, self.theta_noise_level)
            # self.theta += noise

    def sense(self):
        obstacles = self.env.get_obstacles()
        robot_pose = self.get_robot_pose()
        self.sensor.generate_beam_and_measure(robot_pose, obstacles)
        self.update_internal_map()

    # this is in fact what a robot can predict about its own future position
    def _odometer(self, delta_time):
        left_angular_velocity = self.left_motor_speed
        right_angular_velocity = self.right_motor_speed

        v_x = cos(self.theta) * (self.wheel_radius * (left_angular_velocity + right_angular_velocity) / 2)
        v_y = sin(self.theta) * (self.wheel_radius * (left_angular_velocity + right_angular_velocity) / 2)
        omega = (self.wheel_radius * (left_angular_velocity - right_angular_velocity)) / self.axel_length

        next_x = self.x + (v_x * delta_time)
        next_y = self.y + (v_y * delta_time)
        next_theta = self.theta + (omega * delta_time)

        # Ensure the orientation stays within the range [0, 2*pi)
        next_theta = next_theta % (2 * pi)

        return RobotPose(next_x, next_y, next_theta)


    def get_robot_pose(self):
        return RobotPose(self.x, self.y, self.theta)

    def get_robot_radius(self):
        return self.axel_length/2

    def draw(self, surface):
        pygame.draw.circle(surface, (0,255,0), center=(self.x, self.y), radius=self.axel_length/2, width = 1)

        # Calculate the left and right wheel positions
        half_axl = self.axel_length/2
        left_wheel_x = self.x - half_axl * sin(self.theta)
        left_wheel_y = self.y + half_axl * cos(self.theta)
        right_wheel_x = self.x + half_axl * sin(self.theta)
        right_wheel_y = self.y - half_axl * cos(self.theta)

        # Calculate the heading line end point
        heading_length = half_axl + 2
        heading_x = self.x + heading_length * cos(self.theta)
        heading_y = self.y + heading_length * sin(self.theta)

        # Draw the axle line
        pygame.draw.line(surface, (0, 255, 0), (left_wheel_x, left_wheel_y), (right_wheel_x, right_wheel_y), 3)

        # Draw the heading line
        pygame.draw.line(surface, (255, 0, 0), (self.x, self.y), (heading_x, heading_y), 5)

        # Draw sensor beams
        self.sensor.draw(self.get_robot_pose(),surface)

    # update_internal_map
    def update_internal_map(self):
        # Where are we?
        x = int(self.x)
        y = int(self.y)
        # how much area do we cover?
        msd = self.max_sensor_distance
        # Define area that we can potentially see - for now we pretend it is square
        x_lower_bound = max(0, x - msd)
        x_upper_bound = min(self.env.width, x + msd)
        y_lower_bound = max(0, y - msd)
        y_upper_bound = min(self.env.height, y + msd)
        for i in range(x_lower_bound,x_upper_bound):
            # Perhaps calculate how far the beam is reaching and use that as upper bound for obstacle detection.
            for j in range(y_lower_bound, y_upper_bound):
                # if there is an object, stop detecting.
                # Q: Is there a risk of missing an obstacle?
                # If we or on the other side of an obstacle we have come too far
                # - There is some logic of for this in the sensor class.
                self.floor_plan[i][j] += 1
        print(self.floor_plan[x][y])
        # TODO Make intersection function - consider using shapely like in sensor.
        # TODO: Have we been there before? Update if we have not, return if we have completed everything and calculate percentage discovered
    # TODO: calculate percentage discovered