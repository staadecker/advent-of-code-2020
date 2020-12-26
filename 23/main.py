class Cup:
    def __init__(self, value, next):
        self.value = value
        self.next = next

class CircularArray:
    def __init__(self, arr):
        self.len = len(arr)
        self.arr = arr
        self.mapping = {}

        for i in range(len(arr)):
            self.mapping[arr[i]] = i

    def index(self, value):
        return self.mapping[value]

    def move_forward(self, from_i, to_i):
        value = self.arr.pop(from_i)
        self.arr.insert(to_i, value)

        for i in range(from_i, to_i):
            self.mapping[self.arr[i]] -= 1
        self.mapping[value] = to_i

    def move_back(self, from_i, to_i):
        value = self.arr.pop(from_i)
        self.arr.insert(to_i + 1, value)

        for i in range(to_i + 2, from_i + 1):
            self.mapping[self.arr[i]] += 1
        self.mapping[value] = to_i + 1

    def move_one(self, from_i, to_i):
        self.move_forward(from_i, to_i) if from_i < to_i else self.move_back(from_i, to_i)

    def move_three(self, from_i, to_i):
        offset = 0
        for _ in range(3):
            self.move_one(from_i % self.len, to_i % self.len)
            if from_i > to_i:
                from_i = (from_i + 1) % self.len
                to_i = (to_i + 1) % self.len
        self.verify()

    def __getitem__(self, item):
        return self.arr[item]

    def verify(self):
        for i, x in enumerate(self.arr):
            if self.mapping[x] != i:
                raise ValueError(f"Incorrect value for {x} at {i}")
        return True


class Game:
    def __init__(self, cups):
        self.cups = CircularArray(cups)
        self.current_cup = cups[0]
        self.smallest_cup = min(cups)
        self.largest_cup = max(cups)
        self.num_cups = len(cups)

    def play_turn(self):
        to_remove_i = self.cups.index(self.current_cup) + 1
        destination_value = self.current_cup

        # Find destination
        while True:
            destination_value -= 1
            if destination_value < self.smallest_cup:
                destination_value = self.largest_cup

            destination_index = self.cups.index(destination_value)
            if to_remove_i <= self.num_cups - 3 and to_remove_i <= destination_index < to_remove_i + 3:
                continue
            elif to_remove_i > self.num_cups - 3:
                if destination_index >= to_remove_i:
                    continue
                if destination_index < (to_remove_i + 3) % self.num_cups:
                    continue

            break

        # print(self.current_cup, destination_value, self.cups.arr)
        self.cups.move_three(to_remove_i, destination_index)
        self.current_cup = self.cups[(self.cups.index(self.current_cup) + 1) % self.num_cups]

    def play(self, turns):
        for _ in range(turns):
            self.play_turn()


def main(filename):
    game = read_input(filename)
    game.play(10)
    print(game.cups.arr)


def read_input(filename):
    with open(filename, "r") as f:
        cups = list(map(int, list(f.read().strip())))
    return Game(cups)


if __name__ == '__main__':
    filename = "sample_input.txt"
    main(filename)
