def main(filename):
    door_public, card_public = read_input(filename)
    door_loop, card_loop = find_loop_size(door_public, card_public)
    print(door_loop, card_loop)
    encryption_key = encrypt(door_public, card_loop)
    print(encryption_key)


def read_input(filename):
    with open(filename, "r") as f:
        keys = list(map(int, f.read().strip().split("\n")))

    return keys


def find_loop_size(door_public, card_public):
    value = 1
    loop = 0
    door_loop = None
    card_loop = None
    while True:
        value = (value * 7) % 20201227
        loop += 1
        if door_loop is None and value == door_public:
            door_loop = loop
        if card_loop is None and value == card_public:
            card_loop = loop
        if card_loop and door_loop:
            break
    return door_loop, card_loop


def encrypt(key, loop):
    value = 1
    for _ in range(loop):
        value = (value * key) % 20201227
    return value


if __name__ == '__main__':
    filename = "input.txt"
    main(filename)
