import pygame
from pygame.locals import KEYDOWN, QUIT

from simulator import Simulator
from visualizer import Visualizer

#for potential visualization
USE_VISUALIZATION = True

# to pause the execution
PAUSE = False

# Initialize Pygame
pygame.init()

# Set up environment
width, height = 1200, 800 # cm

simulator = Simulator(width, height)

if USE_VISUALIZATION:
    visualizer = Visualizer(width, height)

def main():
    global USE_VISUALIZATION, PAUSE
    start_time = pygame.time.get_ticks()
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            if event.type == KEYDOWN:
                if event.key == pygame.K_h: # use space key to toggle between visualization and headless
                    USE_VISUALIZATION = not USE_VISUALIZATION
                    print("Visualization is", "on" if USE_VISUALIZATION else "off")
                if event.key == pygame.K_SPACE:
                    PAUSE = not PAUSE
        

        if not PAUSE:
            # simulate one execution cycle of the robot
            simulator.run_tick()

        if USE_VISUALIZATION:
            visualizer.visualize(simulator.env, simulator.robot)



    print("total execution time:", (pygame.time.get_ticks() - start_time) / 1000, "seconds")  # runtime in seconds

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()