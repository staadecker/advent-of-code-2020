FILE = "sample_input.txt"


class DirectionalEdge:
    def __init__(self, value, to_tile=None, tile_side=None, is_flipped=None):
        self.value = value
        self.to_tile = to_tile
        self.tile_side = tile_side
        self.is_flipped = is_flipped

    def __repr__(self):
        return self.value if self.to_tile is None else f"{self.to_tile.tile_id}:{self.is_flipped}"

    def __str__(self):
        return self.__repr__()


class Tile:
    def __init__(self, tile_id, left, right, top, down, content):
        self.tile_id = tile_id
        self.edges = [DirectionalEdge(left), DirectionalEdge(top), DirectionalEdge(right), DirectionalEdge(down)]
        self.missing_edges = 0
        self.rotate = 0
        self.flipped_about_y = False
        self.flipped_about_x = False
        self.content = content

    def get_edges(self):
        return [self.get_edge(i) for i in range(4)]

    def __repr__(self):
        return f"{self.tile_id}->{self.get_edges()}"

    def __str__(self):
        return self.__repr__()

    def get_edge(self, side):
        i = side
        if self.flipped_about_x and side % 2 == 1:
            i += 2
        if self.flipped_about_y and side % 2 == 0:
            i += 2

        i -= self.rotate
        return self.edges[i % 4]

    def flip_over_y(self, arr):
        return [row[::-1] for row in arr]

    def rotate_right(self, arr):
        new = []
        for j in range(len(arr[0])):
            new.append("".join([arr[i][j] for i in range(len(arr) - 1, -1, -1)]))
        return new

    def get_content(self):
        new = self.content[:]
        for i in range(self.rotate):
            new = self.rotate_right(new)
        if self.flipped_about_y:
            new = self.flip_over_y(new)
        if self.flipped_about_x:
            new = new[::-1]
        return new

    def has_flip(self):
        return self.flipped_about_x or self.flipped_about_y


def make_tile(tile_input):
    lines = tile_input.split("\n")
    tile_id = int(lines[0].split(" ")[1][:-1])
    tile_content = lines[1:]
    content = list(map(lambda r: r[1:-1], tile_content[1:-1]))

    return Tile(
        tile_id,
        "".join(list(map(lambda r: r[0], tile_content)))[::-1],
        "".join(list(map(lambda r: r[-1], tile_content))),
        tile_content[0],
        tile_content[-1][::-1],
        content
    )


def main():
    with open(FILE, "r") as f:
        tiles = list(map(make_tile, f.read().strip().split("\n\n")))

    connect_tiles(tiles)
    generate_stats(tiles)
    grid = make_grid(tiles)

    # print(tiles)
    print(grid)
    print([list(map(lambda t: t.tile_id, row)) for row in grid])
    print([list(map(lambda t: t.flipped_about_y, row)) for row in grid])
    print([list(map(lambda t: t.flipped_about_x, row)) for row in grid])
    verify_grid(grid)

    # grid = flip_2d_array(grid)
    grid_content = join_tiles(grid)


    print("\n".join(grid_content))
    print()
    # print("\n".join(flip_2d_array(grid_content)))


def flip_2d_array(arr):
    new = []
    for j in range(len(arr[0])):
        new_row = []
        for i in range(len(arr)):
            new_row.append(arr[i][j])
        new.append(new_row)
    return new


def connect_tiles(tiles):
    all_edges = {}
    for tile in tiles:
        for i, edge in enumerate(tile.edges):
            edge_value = edge.value
            for is_flipped, value in enumerate([edge_value, edge_value[::-1]]):
                is_flipped = bool(is_flipped)
                previous_edge = all_edges.pop(value, None)
                # First of the pair
                if previous_edge is None:
                    # Don't add flipped edges
                    if not is_flipped:
                        all_edges[edge_value] = DirectionalEdge(edge_value, tile, i)
                else:
                    tile.edges[i] = previous_edge
                    tile.edges[i].is_flipped = is_flipped
                    previous_side = previous_edge.tile_side
                    previous_edge.to_tile.edges[previous_side] = \
                        DirectionalEdge(edge_value, tile, i, previous_edge.is_flipped)

    for tile in tiles:
        for i in range(4):
            if tile.edges[i].to_tile is None:
                tile.edges[i] = None
                tile.missing_edges += 1


def generate_stats(tiles):
    missing_edges = {0: 0, 1: 0, 2: 0}
    for tile in tiles:
        missing_edges[tile.missing_edges] += 1
    print(f"Missing edges {missing_edges}")


def find_corner_tile(tiles):
    for tile in tiles:
        if tile.missing_edges == 2:
            tile.flipped_about_x = True
            return tile


def find_tile_from_left(left_tile):
    edge = left_tile.get_edge(2)
    tile = edge.to_tile
    tile.rotate = (4 - edge.tile_side) % 4
    tile.flipped_about_x = edge.is_flipped == left_tile.has_flip()
    return tile


def find_tile_from_top(top_tile):
    edge = top_tile.get_edge(3)
    tile = edge.to_tile
    tile.flipped_about_y = edge.is_flipped == top_tile.has_flip()
    tile.rotate = (5 - edge.tile_side) % 4
    return tile


def make_grid(tiles):
    width = int(len(tiles) ** 0.5)

    grid = [[None] * width for _ in range(width)]

    for i in range(width):
        for j in range(width):
            if i == 0 and j == 0:
                tile = find_corner_tile(tiles)
            elif i == 0:
                tile = find_tile_from_left(grid[0][j - 1])
            else:
                tile = find_tile_from_top(grid[i - 1][j])
            grid[i][j] = tile
    return grid


def verify_grid(grid):
    for i in range(len(grid)):
        if grid[0][i].get_edge(1) is not None:
            raise Exception(f"0, {i}")
        if grid[-1][i].get_edge(3) is not None:
            raise Exception(f"-1, {i}")
        if grid[i][0].get_edge(0) is not None:
            raise Exception(f"{i}, 0")
        if grid[i][-1].get_edge(2) is not None:
            raise Exception(f"{i}, -1")


def join_tiles(grid):
    tiled_content = []

    width = len(grid)

    for i in range(width):
        row = []
        for j in range(width):
            row.append(grid[i][j].get_content())
        tiled_content.append(row)

    grid_content = []

    content_len = len(grid[0][0].content)

    for i in range(width):
        for content_row in range(content_len):
            row = ""
            for j in range(width):
                row += tiled_content[i][j][content_row]
                # row += " "
            grid_content.append(row)
        # grid_content.append(" ")

    return grid_content


if __name__ == '__main__':
    main()
