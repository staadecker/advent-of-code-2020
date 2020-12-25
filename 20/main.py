class Tile:
    def __init__(self, tile_id, edges):
        self.tile_id = tile_id
        self.edges = edges
        self.num_edges_existing = 0

    def __repr__(self):
        return str(self.tile_id) + ":" + str(4 - self.num_edges_existing)

    def __str__(self):
        return self.__repr__()


def make_tile(tile_input):
    lines = tile_input.split("\n")
    tile_id = int(lines[0].split(" ")[1][:-1])
    tile_content = lines[1:]

    edges = [
        tile_content[0],
        tile_content[-1],
        "".join(list(map(lambda r: r[0], tile_content))),
        "".join(list(map(lambda r: r[-1], tile_content)))
    ]

    return Tile(tile_id, edges)


def main():
    FILE = "sample_input.txt"
    with open(FILE, "r") as f:
        tiles = list(map(make_tile, f.read().strip().split("\n\n")))

    all_edges = {}

    for tile in tiles:
        for edge in tile.edges:
            if edge not in all_edges:
                all_edges[edge] = []
            all_edges[edge].append(tile.tile_id)

            flipped_edge = edge[::-1]
            if flipped_edge not in all_edges:
                all_edges[flipped_edge] = []
            all_edges[flipped_edge].append(tile.tile_id)

    print(all_edges)

    corner_count = 0
    corner_product = 1

    for tile in tiles:
        for edge in tile.edges:
            if len(all_edges[edge]) > 1:
                tile.num_edges_existing += 1

        if tile.num_edges_existing == 2:
            corner_count +=1
            corner_product *= tile.tile_id

    print(corner_count)
    print(corner_product)

    print(tiles)

    width = len(tiles) ** 0.5
    print(width)


if __name__ == '__main__':
    main()
