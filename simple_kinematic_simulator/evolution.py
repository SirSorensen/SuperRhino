"""
Evolutionary algorithm for evolving BaselineController parameters for wall-following.

Module 6: Evolutionary Setup
"""

import random
import statistics
from controllers import BaselineController
from simulator import Simulator

# Parameter bounds
MIN_BASE_SPEED = 0.1
MAX_BASE_SPEED = 5.0
MIN_DESIRED_DISTANCE = 5.0
MAX_DESIRED_DISTANCE = 200.0
MIN_KP = 0.01
MAX_KP = 5.0

# Evolutionary algorithm settings
POPULATION_SIZE = 20
GENERATIONS = 30
ELITE_SIZE = 2
STEPS_PER_EVAL = 100  # number of simulation ticks per evaluation
TIMESTEP = 0.1  # simulation timestep (s)
COLLISION_PENALTY = 1000.0

# Mutation standard deviations per gene
SIGMA_BASE_SPEED = (MAX_BASE_SPEED - MIN_BASE_SPEED) * 0.1
SIGMA_DESIRED_DISTANCE = (MAX_DESIRED_DISTANCE - MIN_DESIRED_DISTANCE) * 0.1
SIGMA_KP = (MAX_KP - MIN_KP) * 0.1

def random_genome():
    """Generate a random genome within parameter bounds."""
    return [
        random.uniform(MIN_BASE_SPEED, MAX_BASE_SPEED),
        random.uniform(MIN_DESIRED_DISTANCE, MAX_DESIRED_DISTANCE),
        random.uniform(MIN_KP, MAX_KP),
    ]

def mutate_genome(genome):
    """Mutate a genome by adding Gaussian noise and clamping to bounds."""
    base, desired, kp = genome
    base = min(max(base + random.gauss(0, SIGMA_BASE_SPEED), MIN_BASE_SPEED), MAX_BASE_SPEED)
    desired = min(max(desired + random.gauss(0, SIGMA_DESIRED_DISTANCE), MIN_DESIRED_DISTANCE), MAX_DESIRED_DISTANCE)
    kp = min(max(kp + random.gauss(0, SIGMA_KP), MIN_KP), MAX_KP)
    return [base, desired, kp]

def evaluate_genome(genome, width=1200, height=800):
    """Evaluate a genome by simulating a robot and computing fitness."""
    # Create controller and simulator
    controller = BaselineController(base_speed=genome[0], desired_distance=genome[1], k_p=genome[2])
    sim = Simulator(width, height, controller=controller)
    errors = []
    collided = False
    for _ in range(STEPS_PER_EVAL):
        sim.run_tick()
        # Measure distance from left sensor
        reading = sim.robot.left_sensor.latest_reading
        if reading:
            dist = reading[0]
            errors.append(abs(dist - genome[1]))
        if sim.robot.collided:
            collided = True
            break
    # Compute fitness: negative average error, heavy penalty on collision
    if collided:
        return -COLLISION_PENALTY
    avg_error = statistics.mean(errors) if errors else float('inf')
    return -avg_error

def evolve():
    """Run the evolutionary algorithm and return the best genome and its fitness."""
    # Initialize population
    population = [random_genome() for _ in range(POPULATION_SIZE)]
    for gen in range(1, GENERATIONS + 1):
        # Evaluate all genomes
        fitnesses = [evaluate_genome(g) for g in population]
        # Pair and sort by fitness (higher is better)
        pop_fit = list(zip(population, fitnesses))
        pop_fit.sort(key=lambda x: x[1], reverse=True)
        best_genome, best_fit = pop_fit[0]
        avg_fit = statistics.mean(fitnesses)
        print(f"Generation {gen}: Best Fitness={best_fit:.3f}, Avg Fitness={avg_fit:.3f}, Best Genome={best_genome}")
        # Select elites
        elites = [g for g, _ in pop_fit[:ELITE_SIZE]]
        # Create next generation: keep elites and fill rest by mutation
        new_population = elites.copy()
        while len(new_population) < POPULATION_SIZE:
            parent = random.choice(elites)
            child = mutate_genome(parent)
            new_population.append(child)
        population = new_population
    # Final evaluation of best individual
    final_fitnesses = [evaluate_genome(g) for g in population]
    pop_fit = list(zip(population, final_fitnesses))
    pop_fit.sort(key=lambda x: x[1], reverse=True)
    best_genome, best_fit = pop_fit[0]
    print(f"\nEvolution complete. Best Fitness={best_fit:.3f}, Best Genome={best_genome}")
    return best_genome, best_fit

if __name__ == '__main__':
    evolve()