class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class CircularArray:
    def __init__(self, arr):
        self.mapping = list(map(Node, range(1, 1000001)))

        previous = self.mapping[-1]  # use last to make it circular

        for x in arr:
            previous.next = self.find(x)
            previous = self.find(x)

        for x in range(max(arr) + 1, 1000001):
            previous.next = self.find(x)
            previous = self.find(x)

    def find(self, value):
        return self.mapping[value - 1]

    def format(self):
        output = ""
        cur = self.find(1).next
        while cur.value != 1:
            output += str(cur.value) + ","
            cur = cur.next
        return output


class Game:
    def __init__(self, cups):
        self.cups = CircularArray(cups)
        self.current_cup = self.cups.find(cups[0])
        self.smallest_cup = min(cups)
        self.largest_cup = 1000000
        self.num_cups = len(cups)

    def play(self, turns):
        for _ in range(turns):
            first_cup = self.current_cup.next
            second_cup = first_cup.next
            third_cup = second_cup.next
            removed_cup_values = (first_cup.value, second_cup.value, third_cup.value)
            destination_value = self.current_cup.value - 1

            # Find destination
            while True:
                if destination_value < self.smallest_cup:
                    destination_value = self.largest_cup

                if destination_value not in removed_cup_values:
                    break

                destination_value -= 1

            # print(self.current_cup.value, destination_value, self.cups.format())
            destination_cup = self.cups.find(destination_value)
            self.current_cup.next = third_cup.next
            third_cup.next = destination_cup.next
            destination_cup.next = first_cup

            # Increment
            self.current_cup = self.current_cup.next


def main(filename):
    game = read_input(filename)
    game.play(10000000)
    # print(game.cups.format())
    first_cup = game.cups.find(1).next
    value1 = first_cup.value
    value2 = first_cup.next.value
    print(value1 * value2, value1, value2)


def read_input(filename):
    with open(filename, "r") as f:
        cups = list(map(int, list(f.read().strip())))
    return Game(cups)


if __name__ == '__main__':
    filename = "input.txt"
    main(filename)
