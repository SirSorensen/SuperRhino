try:
    import pygame
except ImportError:
    pygame = None
from environment import Environment

class Visualizer:
    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Robot Kinematic Simulator")

    def visualize(self, env : Environment, robot):
        self.screen.fill((0, 0, 0))
        # draw environment
        env.draw(self.screen)
        # draw robot
        robot.draw(self.screen)

        # warn the user if collision happened
        if robot.collided:
            print("Collision!")
            # Draw the animation
            self.drawBoom()

        pygame.display.flip()
        pygame.display.update()

    def drawBoom(self):
        font = pygame.font.SysFont("comicsansms", 172)  # pygame.font.Font(self.font, size)
        text_surface = font.render('BOOM', True, (255, 0, 0))

        width = self.screen.get_width()
        height = self.screen.get_height()
        text_rect = text_surface.get_rect(center=(width/2, height/2))

        self.screen.blit(text_surface, text_rect)