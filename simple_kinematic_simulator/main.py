from evolution import Evolution

# Set up environment
width, height = 1200, 800 # cm

evolution = Evolution()

def main():
    evolution.use_visualization = False
    print("\nRound 1! FIGHT!")
    results = evolution.run_cycle(width, height, None)
    last_best = Evolution.find_best_result(results)

    print("\nRound 2... FIGHT!")
    results = evolution.run_cycle(width, height, last_best)
    last_best = Evolution.find_best_result(results)

    print("\nFinal Round!! FIGHT!")
    results = evolution.run_cycle(width, height, last_best)
    last_best = Evolution.find_best_result(results)




if __name__ == "__main__":
    main()