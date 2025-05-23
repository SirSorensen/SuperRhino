import pygame
from Simulator.simulator import Simulator
import random
from Simulator.visualizer import Visualizer
from Simulator.sim_state import SimulatorState

class Evolution:
    def __init__(self, width, height, population_size = 5, use_visualization = True, seed = 42):
        # Init random
        random.seed(seed)
        # Init population
        self.population : list[Simulator] = []
        for _ in range(population_size):
            i = random.uniform(0, 1)
            self.population.append(Simulator(width, height, i=i))
        # Configure the use of visualization
        self.use_visualization = use_visualization
        if self.use_visualization:
            self.visualizer = Visualizer(width, height)


    def run_cycle(self):
        # Initialize Pygame
        pygame.init()
        results : list[SimulatorState] = []

        for sim in self.population:
            results.append(self.game_loop(sim))

        Evolution.print_final_result(results)
        # Quit Pygame
        pygame.quit()


    def game_loop(self, sim : Simulator):
        start_time = pygame.time.get_ticks()

        # Game loop
        while self.get_cycle_time(start_time) <= 5:
            # simulate one execution cycle of the robot
            sim.run_tick()

            if self.use_visualization:
                self.visualizer.visualize(sim.env, sim.robot)

        print("\ntotal execution time:", self.get_cycle_time(start_time), "seconds")  # runtime in seconds

        sim_state : SimulatorState = sim.get_state()
        return sim_state


    def get_cycle_time(self, start_time):
        return (pygame.time.get_ticks() - start_time) / 1000


    def print_final_result(results : list[SimulatorState]):
        print("\n================\n")
        print("Final results:")
        i = 0
        for r in results:
            print(f"Results from sim {i}")
            r.print_coefficients()
            r.print_result()
            i += 1
        print("\n================\n")