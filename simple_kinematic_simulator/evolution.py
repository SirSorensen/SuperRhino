import pygame
from Simulator.simulator import Simulator
import random
from Simulator.visualizer import Visualizer
from Simulator.sim_state import SimulatorState

class Evolution:
    def __init__(self, population_size = 5, use_visualization = True, seed = 42):
        # Init random
        random.seed(seed)
        # Init population
        self.population_size = population_size
        # Configure the use of visualization
        self.use_visualization = use_visualization


    def run_cycle(self, width, height, last_best : SimulatorState):
        # Initialize Pygame
        pygame.init()
        if self.use_visualization:
            self.visualizer = Visualizer(width, height)

        population : list[Simulator] = []
        for _ in range(self.population_size):
            i = Evolution.gen_parameters(last_best)
            population.append(Simulator(width, height, i=i))

        results : list[SimulatorState] = []

        for sim in population:
            results.append(self.game_loop(sim))

        Evolution.print_final_result(results)
        # Quit Pygame
        pygame.quit()
        return results


    def run_single(self, width, height, sim : Simulator):
        # Initialize Pygame
        pygame.init()
        if self.use_visualization:
            self.visualizer = Visualizer(width, height)

        self.game_loop(sim)

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

            if sim.robot.collided:
                print("\nAborting! Robot colided with wall!")
                sim_state : SimulatorState = sim.get_state()
                sim_state.robot_mid_dist = 99999999
                print("total execution time:", self.get_cycle_time(start_time), "seconds")  # runtime in seconds
                return sim_state

        print("\ntotal execution time:", self.get_cycle_time(start_time), "seconds")  # runtime in seconds

        sim_state : SimulatorState = sim.get_state()
        return sim_state


    def get_cycle_time(self, start_time):
        return (pygame.time.get_ticks() - start_time) / 1000


    def gen_parameters(last_best : SimulatorState):
        if last_best is None:
            return random.uniform(0, 1)
        else:
            return max(0, last_best.robot_i + random.uniform(-0.1, 0.1))


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


    def find_best_result(results : list[SimulatorState]):
        best = min(results, key=lambda r: r.robot_mid_dist)
        print(f"\nBest found at index {results.index(best)}")
        best.print_coefficients()
        return best
