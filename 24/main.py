def main(filename):
    instructions = read_input(filename)
    # print(instructions)
    tiles = run_instructions(instructions)
    # print(tiles)
    count = count_black(tiles)
    print_tiles(tiles)
    print()
    print(count)
    for i in range(100):
        flips = determine_flips(tiles)
        tiles = apply_flips(tiles, flips)
        print(i, count_black(tiles))
        # print_tiles(tiles)


def read_input(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

    instructions = []
    for line in lines:
        instruction = []
        i = 0
        while i < len(line):
            c = line[i]
            if c == "s" or c == "n":
                instruction.append(line[i:i + 2])
                i += 2
            else:
                instruction.append(line[i])
                i += 1
        instructions.append(instruction)

    return instructions


def run_instructions(instructions):
    tiles = {}

    for sequence in instructions:
        # Axis are downwards is positive y and rightwards is positive x
        x, y = 0, 0
        for move in sequence:
            even = y % 2 == 0
            if move == "ne":
                y -= 1
                if not even:
                    x += 1
            elif move == "nw":
                y -= 1
                if even:
                    x -= 1
            elif move == "sw":
                y += 1
                if even:
                    x -= 1
            elif move == "se":
                y += 1
                if not even:
                    x += 1
            elif move == "e":
                x += 1
            elif move == "w":
                x -= 1
            else:
                raise RuntimeError(f"Don't know what move is: {move}")
        if (x, y) not in tiles:
            tiles[(x, y)] = True
        else:
            tiles[(x, y)] = not tiles[(x, y)]

    return tiles


def count_black(tiles):
    count = 0
    for tile in tiles.values():
        if tile:
            count += 1
    return count


def add_coord(a, b):
    return a[0] + b[0], a[1] + b[1]


def determine_flips(tiles):
    even_offsets = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0))
    odd_offsets = ((-1, 0), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    white_tiles = {}
    flips = set()
    for tile, flipped in tiles.items():
        if flipped:
            # Check black tile
            black_neighbours = 0
            offsets = even_offsets if tile[1] % 2 == 0 else odd_offsets
            for offset in offsets:
                neighbour = add_coord(tile, offset)
                if neighbour in tiles and tiles[neighbour]:
                    black_neighbours += 1
                else:
                    if neighbour not in white_tiles:
                        white_tiles[neighbour] = 1
                    else:
                        white_tiles[neighbour] += 1
            if black_neighbours == 0 or black_neighbours > 2:
                flips.add(tile)

    # print(white_tiles)
    for white_tile, count in white_tiles.items():
        if count == 2:
            flips.add(white_tile)

    return flips


def apply_flips(tiles, flips):
    for tile in flips:
        if tile not in tiles:
            tiles[tile] = True
        else:
            tiles[tile] = not tiles[tile]
    return tiles


def print_tiles(tiles):
    minx = min(min(tiles, key=lambda xy: xy[0])[0], -1)
    maxx = max(max(tiles, key=lambda xy: xy[0])[0], 1)
    miny = min(min(tiles, key=lambda xy: xy[1])[1], -1)
    maxy = max(max(tiles, key=lambda xy: xy[1])[1], 1)

    for y in range(miny, maxy + 1):
        print(y, end="\t")
        if y % 2 == 1:
            print(" ", end="")
        for x in range(minx, maxx + 1):
            is_origin = (x, y) == (0, 0)
            if (x, y) in tiles and tiles[(x, y)]:
                print("O" if is_origin else "#", end="")
            else:
                print("o" if is_origin else ".", end="")
            print(" ", end="")
        print()


if __name__ == '__main__':
    filename = "input.txt"
    main(filename)
