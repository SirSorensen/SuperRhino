import pygame
from evolution import Evolution

# Set up environment
width, height = 1200, 800 # cm

evolution = Evolution(width, height)

def main():
    evolution.run_cycle()

if __name__ == "__main__":
    main()