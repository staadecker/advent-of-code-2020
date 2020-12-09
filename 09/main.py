FILENAME = "input.txt"
PREAMBLE_LEN = 25


class DataGrid:
    def __init__(self, data):
        self.grid = []
        self.data = data

        for i in range(len(data)):
            self.grid.append([-1] * len(data))

    def get(self, i, j):
        if i == j:
            raise RuntimeError("Can't sum two same numbers.")
        if self.grid[i][j] == -1:
            a, b = self.data[i], self.data[j]
            self.grid[i][j] = a + b if a != b else None
        return self.grid[i][j]


def main():
    with open(FILENAME, "r") as f:
        data = list(map(lambda row: int(row), f.readlines()))

    grid = DataGrid(data)

    offset = 0
    invalid = None

    while offset + PREAMBLE_LEN < len(data):
        valid = False
        target = data[offset + PREAMBLE_LEN]
        for i in range(offset, offset + PREAMBLE_LEN):
            for j in range(offset, offset + PREAMBLE_LEN):
                if i != j and grid.get(i, j) == target:
                    valid = True
                    break
            if valid:
                break

        if not valid:
            invalid = target
            break

        offset += 1

    if invalid is None:
        raise RuntimeError("No invalid number found")

    start = 0
    end = 0
    runningSum = 0

    while True:
        if runningSum < invalid:
            runningSum += data[end]
            end += 1
            if end > len(data):
                break
        elif runningSum > invalid:
            runningSum -= data[start]
            start += 1
        else:
            break

    print(invalid)
    invalid_set = data[start:end]
    print(min(invalid_set) + max(invalid_set))


if __name__ == '__main__':
    main()
