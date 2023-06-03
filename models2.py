
from constants import Symbol


class SwapError(Exception):

    def __init__(self, entity1, entity2):
        super().__init__(
            f'Cannot swap {repr(entity1)} and {repr(entity2)}.'
        )


class Entity:

    def __init__(self, coords, movable=True):
        self.coords = coords
        self.movable = movable

    def is_neighbour(self, entity):
        x1, y1 = self.coords
        x2, y2 = entity.coords
        return abs((x1 - x2) + (y1 - y2)) == 1

    def __repr__(self):
        x, y = self.coords
        return f'<{self.__class__.__name__} x={x} y={y}>'


class Worker(Entity):

    def __init__(self, coords, current_entity):
        super().__init__(coords, movable=False)
        self._current_entity = current_entity

    @property
    def current_entity(self):
        return self._current_entity

    @current_entity.setter
    def current_entity(self, entity):
        if isinstance(entity, Package):
            if not entity.ordered:
                self._current_entity = entity
            else:
                raise ValueError(
                    f'Invalid value {repr(entity)} for current entity.'
                )
        elif isinstance(entity, Empty):
            self._current_entity = entity
        else:
            raise ValueError(
                f'Invalid value {repr(entity)} for current entity.'
            )

    @property
    def busy(self):
        if isinstance(self.current_entity, Package):
            return True
        elif isinstance(self.current_entity, Empty):
            return False

    def __str__(self):
        if self.busy:
            return Symbol.BUSY_WORKER
        else:
            return Symbol.IDLE_WORKER


class Package(Entity):

    def __init__(self, coords, ordered=False):
        super().__init__(coords, movable=True)
        self.ordered = ordered

    def __str__(self):
        if self.ordered:
            return Symbol.ORDERED_PACKAGE
        else:
            return Symbol.PACKAGE


class Empty(Entity):

    def __init__(self, coords):
        super().__init__(coords, movable=False)

    def __str__(self):
        return Symbol.EMPTY


class Grid:

    def __init__(self, data):
        self.workers = []
        self.ordered_packages = []
        self.unordered_packages = []
        self.empty_cells = []

        self.max_x = len(data[0])
        self.max_y = len(data)

        self.order = {
            Empty: 0,
            Package: 1,
            Worker: 2,
        }

        for y, row in enumerate(data):
            for x, symbol in enumerate(row):
                coords = (x, y)
                match symbol:
                    case Symbol.EMPTY:
                        self.empty_cells.append(Empty(coords))
                    case Symbol.PACKAGE:
                        self.unordered_packages.append(Package(coords, ordered=False))
                    case Symbol.ORDERED_PACKAGE:
                        self.ordered_packages.append(Package(coords, ordered=True))
                    case Symbol.IDLE_WORKER:
                        empty_cell = Empty(coords)
                        self.empty_cells.append(empty_cell)
                        self.workers.append(Worker(coords, empty_cell))
                    case Symbol.BUSY_WORKER:
                        package = Package(coords, ordered=False)
                        self.unordered_packages.append(package)
                        self.workers.append(Worker(coords, package))
                    case _:
                        raise ValueError(
                            f'Invalid symbol {symbol}.'
                        )

    def swap(self, entity1, entity2):

        if not entity1.is_neighbour(entity2):
            raise SwapError(entity1, entity2)

        type1, type2 = type(entity1), type(entity2)

        if type1 == type2:
            raise SwapError(entity1, entity2)

        if self.order[type1] < self.order[type2]:
            entity1, entity2 = entity2, entity1
            type1, type2 = type2, type1

        if (type1, type2) == (Package, Empty):
            self.swap_package_with_empty(entity1, entity2)
        elif (type1, type2) == (Worker, Package):
            self.swap_worker_with_package(entity1, entity2)
        else:
            self.swap_worker_with_empty(entity1, entity2)

    def swap_package_with_empty(self, package, empty):
        package.coords, empty.coords = empty.coords, package.coords

    def swap_worker_with_package(self, worker, package):
        if package.ordered:
            if worker.busy:
                raise SwapError(worker, package)
            else:
                self.ordered_packages.remove(package)
                self.empty_cells.append(Empty(package.coords))
        else:
            if worker.busy:
                raise SwapError(worker, package)
            else:
                worker.current_entity.coords, package.coords = package.coords, worker.current_entity.coords
                worker.current_entity = package

    def swap_worker_with_empty(self, worker, empty):
        if worker.busy:
            worker.current_entity.coords, empty.coords = empty.coords, worker.current_entity.coords
            worker.current_entity = empty
        else:
            raise SwapError(worker, empty)

    def __str__(self):
        symbols = [
            ['None' for _ in range(self.max_x)] for _ in range(self.max_y)
        ]

        for entity in (
                self.empty_cells + self.ordered_packages + self.unordered_packages + self.workers
        ):
            x, y = entity.coords
            symbols[y][x] = str(entity)

        return '\n'.join([''.join(row) for row in symbols])


class TransitionGrid:

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.symbols = [[Symbol.EMPTY for _ in range(max_x)] for _ in range(max_y)]

    @staticmethod
    def get_direction(from_entity, to_entity):
        if not from_entity.is_neighbour(to_entity):
            raise SwapError(from_entity, to_entity)

        x1, y1 = from_entity.coords
        x2, y2 = to_entity.coords

        if x1 - x2 == 1:
            return Symbol.LEFT
        elif x1 - x2 == -1:
            return Symbol.RIGHT
        elif y1 - y2 == 1:
            return Symbol.UP
        elif y1 - y2 == -1:
            return Symbol.DOWN
        else:
            raise ValueError(
                f'Cannot return direction symbol from {from_entity} to {to_entity}.'
            )

    def valid_transition(self, from_entity, to_entity):
        symbol = self.get_direction(from_entity, to_entity)
        x, y = from_entity.coords
        neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for neighbour in neighbours:
            try:
                neighbour_symbol = self.symbols[neighbour[1]][neighbour[0]]
                if neighbour_symbol in (symbol, Symbol.EMPTY):
                    return True
                else:
                    return False
            except IndexError:
                pass

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.symbols])
