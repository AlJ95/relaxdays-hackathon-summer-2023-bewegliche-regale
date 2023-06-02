
from typing import Tuple, List


class Grid:

    raw_data: List[List[str]]
    max_x: int
    max_y: int
    workers: list
    movables: list
    empty_cells: list

    def __init__(self, raw_data: List[List[str]]):
        Grid.raw_data = raw_data
        Grid.max_x = len(raw_data[0])
        Grid.max_y = len(raw_data)
        Grid.workers = []
        Grid.movables = []
        Grid.empty_cells = []

        for y, row in enumerate(raw_data):
            for x, cell in enumerate(row):
                if cell == "🙋":
                    Grid.workers.append(Worker((x, y), busy=False))
                    Grid.empty_cells.append(EmptyCell((x, y)))
                elif cell == "👷":
                    Grid.workers.append(Worker((x, y), busy=True))
                    Grid.movables.append(MovableObject((x, y), ordered=False))
                elif cell == "📦":
                    Grid.movables.append(MovableObject((x, y), ordered=False))
                elif cell == "🎁":
                    Grid.movables.append(MovableObject((x, y), ordered=True))
                elif cell == "🟨":
                    Grid.empty_cells.append(EmptyCell((x, y)))

        Grid.print_grid()
        Grid.movables[3].down(Grid.empty_cells[0])
        Grid.print_grid()


    @staticmethod
    def print_grid():
        printed_string = [[None for _ in range(Grid.max_x)] for _ in range(Grid.max_y)]

        for worker in Grid.workers:
            x, y = worker.coords
            printed_string[y][x] = str(worker)

        for movable in Grid.movables:
            x, y = movable.coords
            printed_string[y][x] = str(movable)

        for empty_cell in Grid.empty_cells:
            x, y = empty_cell.coords
            printed_string[y][x] = str(empty_cell)

        return "\n".join(["".join([obj for obj in row]) for row in printed_string])


class Cell:

    def __init__(self, coords: Tuple[int, int]):
        self.coords = coords


class Worker(Cell):

    def __init__(self, coords: Tuple[int, int], busy=False):
        super().__init__(coords)
        self.busy = busy

    def __str__(self):
        if self.busy:
            return "👷"
        else:
            return "🙋"


class EmptyCell(Cell):

    def __init__(self, coords):
        super().__init__(coords)

    def __str__(self):
        return "🟨"


class MovableObject(Cell):

    def __init__(self, coords, ordered=False):
        super().__init__(coords)
        self.ordered = ordered
        self.transitions = []

    def handle_next_cell(self, next_cell: Cell):
        worker_on_cell = [worker.coords for worker in Grid.workers if worker.coords == next_cell.coords]
        if worker_on_cell:
            if self.ordered:
                Grid.empty_cells.append(EmptyCell(self.coords))
                Grid.movables.remove(self)
            else:
                worker_on_cell[0].busy = True

    def up(self, next_cell: Cell):
        self.coords[1] -= 1
        self.transitions.append("⏫")
        next_cell.coords[1] += 1

        self.handle_next_cell(next_cell)

    def down(self, next_cell: Cell):
        self.coords = (self.coords[0], self.coords[1] + 1)
        self.transitions.append("⏬")
        next_cell.coords = (next_cell.coords[0], next_cell.coords[1] - 1)

        self.handle_next_cell(next_cell)

    def left(self, next_cell: Cell):
        self.coords = (self.coords[0] - 1, self.coords[1])
        self.transitions.append("⏪")
        next_cell.coords = (next_cell.coords[0] + 1, next_cell.coords[1])
        self.handle_next_cell(next_cell)

    def right(self, next_cell: Cell):
        self.coords = (self.coords[0] + 1, self.coords[1])
        self.transitions.append("⏩")
        next_cell.coords = (next_cell.coords[0] - 1, next_cell.coords[1])

        self.handle_next_cell(next_cell)

    def do_nothing(self):
        self.transitions.append("🟨")

    def __str__(self):
        if self.ordered:
            return "🎁"
        else:
            return "📦"


if __name__ == '__main__':
    from main import load_json
    data = load_json(0)
    grid = Grid(data)
    print(grid)