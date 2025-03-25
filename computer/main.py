
from labyrinth import Labyrinth

sokoban_map = """
######
#@  .#
# $  #
#.$  #
# $ .#
######
"""
lab = Labyrinth()
grid = lab.parse_sokoban_map(sokoban_map)
solution_str : str = lab.sokoban_solver(grid)
print(solution_str)
rhinotron_coords, _, _ = lab.find_positions(grid)
print(rhinotron_coords)