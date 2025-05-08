"""
Evolutionary algorithm for evolving wall-following controller parameters.

Genome representation:
  [detection_range, wall_follow_target, wall_follow_kp, front_safety_distance]

GA parameters, fitness function, and evolutionary loop.
"""
import random
import copy
import statistics
from environment import Environment
from robot import DifferentialDriveRobot

# Genetic Algorithm parameters
POPULATION_SIZE = 30
GENERATIONS = 50
TOURNAMENT_SIZE = 3
ELITE_SIZE = 2
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.2

# Simulation parameters
SIMULATION_TIME = 30.0  # seconds per trial
TIME_STEP = 0.1         # simulation timestep in seconds

# Environment dimensions (must match main.py defaults)
ENV_WIDTH = 1200
ENV_HEIGHT = 800

def create_individual():
    """Create a random individual (genome) within predefined parameter bounds."""
    detection_range = random.uniform(10.0, 200.0)
    wall_follow_target = random.uniform(10.0, 100.0)
    wall_follow_kp = random.uniform(0.01, 1.0)
    front_safety_distance = random.uniform(10.0, 200.0)
    return [detection_range, wall_follow_target, wall_follow_kp, front_safety_distance]

def simulate(individual, start_pos):
    """
    Run a single simulation trial with given parameters.
    Returns fitness for this trial.
    """
    env = Environment(ENV_WIDTH, ENV_HEIGHT)
    x, y, theta = start_pos
    robot = DifferentialDriveRobot(env, x, y, theta)
    # Set controller parameters from genome
    robot.detection_range = individual[0]
    robot.wall_follow_target = individual[1]
    robot.wall_follow_kp = individual[2]
    robot.front_safety_distance = individual[3]

    acquisition_time = None
    left_distances = []
    collision_count = 0
    t = 0.0
    while t < SIMULATION_TIME:
        robot.move(TIME_STEP)
        # update sensors at new pose
        robot.sense()
        # read distances: sensors[2] is left-side
        readings = [s.latest_reading[0] if s.latest_reading else float('inf') for s in robot.sensors]
        # record collision
        if robot.collided:
            collision_count += 1
        # record acquisition time when switching from search to follow
        if acquisition_time is None and not robot.searching_wall:
            acquisition_time = t
        # collect left-side distances during wall-following
        if not robot.searching_wall:
            left_distances.append(readings[2])
        t += TIME_STEP
    # if no wall acquisition, penalize by max time
    if acquisition_time is None:
        acquisition_time = SIMULATION_TIME

    # compute error metrics
    if left_distances:
        errors = [abs(d - robot.wall_follow_target) for d in left_distances]
        mean_error = statistics.mean(errors)
        variance = statistics.pvariance(left_distances)
    else:
        # no follow period -> heavy penalty
        mean_error = SIMULATION_TIME
        variance = SIMULATION_TIME ** 2

    # cost components
    cost = mean_error + 0.1 * variance + 10.0 * collision_count + 0.01 * acquisition_time
    # higher fitness is better, so return negative cost
    return -cost

def evaluate(individual):
    """Evaluate an individual over multiple starting positions."""
    env = Environment(ENV_WIDTH, ENV_HEIGHT)
    starts = env.get_starting_positions()
    # average fitness across all start positions
    fitnesses = [simulate(individual, pos) for pos in starts]
    return sum(fitnesses) / len(fitnesses)

def tournament_selection(population, fitnesses):
    """Select individuals via tournament selection."""
    selected = []
    for _ in range(len(population)):
        contestants = random.sample(list(zip(population, fitnesses)), TOURNAMENT_SIZE)
        winner = max(contestants, key=lambda cf: cf[1])[0]
        selected.append(copy.deepcopy(winner))
    return selected

def crossover(parent1, parent2):
    """Uniform crossover between two parents."""
    child1, child2 = parent1[:], parent2[:]
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child1[i], child2[i] = child2[i], child1[i]
    return child1, child2

def mutate(individual):
    """Gaussian mutation on each gene with a probability of MUTATION_RATE."""
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            if i == 0:
                individual[i] += random.gauss(0, 10)
                individual[i] = min(max(individual[i], 10.0), 200.0)
            elif i == 1:
                individual[i] += random.gauss(0, 5)
                individual[i] = min(max(individual[i], 10.0), 100.0)
            elif i == 2:
                individual[i] += random.gauss(0, 0.1)
                individual[i] = min(max(individual[i], 0.01), 1.0)
            elif i == 3:
                individual[i] += random.gauss(0, 10)
                individual[i] = min(max(individual[i], 10.0), 200.0)
    return individual

def evolve():
    """Main evolutionary loop."""
    # initialize population
    population = [create_individual() for _ in range(POPULATION_SIZE)]
    best_individual = None
    best_fitness = float('-inf')
    for gen in range(1, GENERATIONS + 1):
        fitnesses = [evaluate(ind) for ind in population]
        # update best
        gen_best = max(zip(population, fitnesses), key=lambda cf: cf[1])
        if gen_best[1] > best_fitness:
            best_individual, best_fitness = gen_best
        print(f"Generation {gen}: Best fitness = {gen_best[1]:.3f}")
        # selection
        mating_pool = tournament_selection(population, fitnesses)
        # create next generation with elites
        next_population = [copy.deepcopy(population[i]) for i in
                           sorted(range(len(population)), key=lambda i: fitnesses[i], reverse=True)[:ELITE_SIZE]]
        # generate offspring
        while len(next_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(mating_pool, 2)
            if random.random() < CROSSOVER_RATE:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]
            next_population.append(mutate(child1))
            if len(next_population) < POPULATION_SIZE:
                next_population.append(mutate(child2))
        population = next_population
    print("\nBest individual:", best_individual)
    print("Best fitness:", best_fitness)
    return best_individual, best_fitness

if __name__ == "__main__":
    evolve()