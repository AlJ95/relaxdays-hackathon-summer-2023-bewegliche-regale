
from models2 import Grid, TransitionGrid
from utilities import load_json


def solve(grid):
    transitions = []
    while grid.ordered_packages:
        transition_grid = TransitionGrid(grid.max_x, grid.max_y)


if __name__ == '__main__':
    input_data = load_json('instance0.json')
    grid = Grid(input_data)
    print(grid)
    print()
    # grid.swap(grid.packages[23], grid.workers[1])
    print(grid)
