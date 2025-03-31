from umath import cos, sin, radians, degrees
from pybricks.tools import vector, Matrix
from pybricks.tools import wait
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port


### Constants  ###
DT = 0.1  # Time step for odometry updates (seconds)

left_motor: Motor = Motor(Port.B, Direction.COUNTERCLOCKWISE) # The motor that drives the left wheel.
right_motor: Motor = Motor(Port.A) # The motor that drives the right wheel.

wheel_radius = 0.028 # Diameter of the wheels (in meters).
axle_track = 0.085 # Distance between the points where both wheels touch the ground (in meters).
L = axle_track / 2

### Dynamic variables ###
x, y = 0.0, 0.0 # Position (in meters)
theta = 0.0 # Orientation (in radians)


def get_wheel_velocities() -> tuple[int, int]:
    """Get wheel angular velocities in radians per second."""
    # use motor.speed() to return the current angular velocity of the motor in degrees per second
    return (radians(left_motor.speed()), radians(right_motor.speed()))

def update_odometry():
    """Update the robot's position using kinematic equations."""
    global x, y, theta
    left_velocity, right_velocity = get_wheel_velocities()

    x_robot = (right_velocity + left_velocity) * (wheel_radius/2) # meters per second
    y_robot = 0 # meters per second
    theta_robot = (right_velocity - left_velocity) * (wheel_radius/(2*L))  # radians per second

    theta += theta_robot * DT # Udate theta

    changes_robot = vector(x_robot, y_robot, theta_robot)

    rotation_matrix = Matrix([
                                [cos(theta), -sin(theta), 0],
                                [sin(theta),  cos(theta), 0],
                                [     0    ,      0     , 1]
                             ])

    changes = rotation_matrix * changes_robot
    x += changes[0] * DT
    y += changes[1] * DT



def move_robot(left_speed, right_speed, duration):
    """Move the robot with given wheel speeds for a given duration and do odometry."""
    left_motor.run(left_speed)
    right_motor.run(right_speed)

    for _ in range(int(duration / DT)):
        update_odometry()
        # print of you want:
        print(x,y,degrees(theta))
        wait(int(DT * 1000))  # Convert seconds to milliseconds

    left_motor.stop()
    right_motor.stop()

_speed=400
# Example movement sequence:
# move forward for n sec
move_robot(_speed, _speed, 3)
# turn in place for m sec
move_robot(-_speed, _speed, 3)
# move forward for k seconds
move_robot(_speed, _speed, 3)
print("Final Position:", x, y, degrees(theta))