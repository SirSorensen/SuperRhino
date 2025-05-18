import pygame
from pygame.locals import QUIT, KEYDOWN
from environment import Environment
import random
from robot import DifferentialDriveRobot
from evolve import evolve

# for potential visualization
USE_VISUALIZATION = True

# to pause the execution
PAUSE = False

# Initialize Pygame
pygame.init()

# Set up environment
width, height = 1200, 800  # cm
env = Environment(width, height)

# (simulated) time taken for one cycle of the robot executing its algorithm
robot_timestep = 0.1  # in seconds (simulated time)

# Choose a starting position near a wall (not directly aligned), possibly facing away
start_positions = env.get_starting_positions()
start_x, start_y, start_theta = random.choice(start_positions)
print(f"Starting position selected: x={start_x}, y={start_y}, theta={start_theta}")

robot = DifferentialDriveRobot(env, start_x, start_y, start_theta)
best_params, best_fitness = evolve()
(
    best_detection_range,
    best_wall_follow_target,
    best_wall_follow_kp,
    best_front_safety_distance,
) = best_params
print(
    f"Evolved parameters: detection_range={best_detection_range}, wall_follow_target={best_wall_follow_target}, wall_follow_kp={best_wall_follow_kp}, front_safety_distance={best_front_safety_distance}, fitness={best_fitness}"
)
robot.detection_range = best_detection_range
robot.wall_follow_target = best_wall_follow_target
robot.wall_follow_kp = best_wall_follow_kp
robot.front_safety_distance = best_front_safety_distance

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Robot Kinematic Simulator")


def main():
    global USE_VISUALIZATION, PAUSE
    collision_count = 0
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if (
                    event.key == pygame.K_h
                ):  # use space key to toggle between visualization and headless
                    USE_VISUALIZATION = not USE_VISUALIZATION
                    print("Visualization is", "on" if USE_VISUALIZATION else "off")
                if event.key == pygame.K_SPACE:
                    PAUSE = not PAUSE
                if event.key == pygame.K_q:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if not PAUSE:
            # simulate one execution cycle of the robot
            robot.move(robot_timestep)

        if USE_VISUALIZATION:
            screen.fill((0, 0, 0))
            # draw environment
            env.draw(screen)
            # draw robot
            robot.draw(screen)

            # warn the user if collision happened
            if robot.collided:
                # Draw the animation
                drawBoom()

                collision_count += 1
                print(f"Collision count: {collision_count}")

            pygame.display.flip()
            pygame.display.update()

    # Quit Pygame
    pygame.quit()


def drawBoom():
    font = pygame.font.SysFont("comicsansms", 172)  # pygame.font.Font(self.font, size)
    text_surface = font.render("BOOM", True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(width / 2, height / 2))
    screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    main()
