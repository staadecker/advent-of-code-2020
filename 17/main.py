import numpy as np

FILENAME = "sample_input.txt"

class NeighbourIterator:
    def __init__(self, pos):
        self.pos = pos
        self.offset = (0, 0, 0)
        self.z = None

    def increment_offset(self):
        oz, ox, oy = self.offset
        oy = (oy + 1) % 3
        if oy == 0:
            ox = (ox + 1) % 3
            if ox == 0:
                oz = (oz + 1) % 3
                if oz == 0:
                    self.offset = None
                    return

        self.offset = (oz, ox, oy)

        # Redo if the offset is the central cell
        if self.offset == (1, 1, 1):
            self.increment_offset()

    def get_pos(self):
        oz, ox, oy = self.offset
        z, x, y = self.pos
        return z - 1 + oz, x - 1 + ox, y - 1 + oy

    def __iter__(self):
        self.offset = (0, 0, 0)
        return self

    def __next__(self):
        if self.offset is None:
            raise StopIteration
        n = self.get_pos()
        self.increment_offset()
        return n


class Grid:
    def __init__(self, height, width, depth, dtype=bool, default=False):
        self.height = height
        self.width = width
        self.depth = depth
        self.pos = None  # [z,x,y]
        self.grid = np.array([[[default] * self.width for _ in range(self.height)] for _ in range(self.depth)],
                             dtype=dtype)

    def next_pos(self, pos):
        (z, x, y) = pos
        y = (y + 1) % self.width
        if y == 0:
            x = (x + 1) % self.height
            if x == 0:
                z = (z + 1) % self.depth
                if z == 0:
                    return None
        return (z, x, y)

    def apply_swap(self, other):
        self.grid = np.bitwise_xor(self.grid, other.grid)

    def count_active(self):
        count = 0
        for cell in self:
            if self[cell]:
                count += 1
        return count

    def __iter__(self):
        self.pos = (0, 0, 0)
        return self

    def __next__(self):
        cur = self.pos
        if cur is None:
            raise StopIteration
        self.pos = self.next_pos(self.pos)
        return cur

    def __getitem__(self, item):
        return self.grid[item]

    def __setitem__(self, key, value):
        self.grid[key] = value

    def __str__(self):
        out = ""
        for z, layer in enumerate(self.grid):
            if np.any(layer):  # Check if anything in the layer is active
                out += f"z={z - 6}\n"
                for row in layer:
                    for c in row:
                        out += str(int(c) if int(c) > 0 else ".")
                    out += "\n"
        return out

    def __repr__(self):
        return self.__str__()


with open(FILENAME) as f:
    raw_input = f.read().strip().split("\n")

height = len(raw_input) + 6 * 2
width = len(raw_input[0]) + 6 * 2
depth = 1 + 6 * 2

grid = Grid(height, width, depth)

# Populate grid with initial values
for x, row in enumerate(raw_input, start=6):
    for y, char in enumerate(row, start=6):
        grid[6, x, y] = char == "#"

# Do 6 passes
for _ in range(6):
    # On each pass loop through every cell
    num_neighbours = Grid(height, width, depth, dtype=int, default=0)
    for cell in grid:
        if grid[cell]:
            for neighbour_pos in NeighbourIterator(cell):
                num_neighbours[neighbour_pos] += 1

    swap = Grid(height, width, depth)
    for cell in grid:
        if grid[cell]:
            swap[cell] = num_neighbours[cell] != 2 and num_neighbours[cell] != 3
        else:
            swap[cell] = num_neighbours[cell] == 3
    grid.apply_swap(swap)

print(grid.count_active())
