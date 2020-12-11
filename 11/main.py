import numpy as np

with open("input.txt", "r") as f:
    seats = np.array(list(map(lambda x: list(x.strip()), f.readlines())))

# Pad seats with floor
seats = np.append(seats, values=[["."] * len(seats[0])], axis=0)  # append row row
seats = np.insert(seats, 0, values=".", axis=0)  # insert row

seats = np.append(seats, values=list(["."] for _ in range(len(seats))), axis=1)
seats = np.insert(seats, 0, values=".", axis=1)

shape = (len(seats), len(seats[0]))

is_seat = np.fromfunction(lambda i, j: seats[i, j] != ".", shape, dtype=int)
state = np.fromfunction(lambda i, j: seats[i, j] == "#", shape, dtype=int)


def find_next_state(state):
    swap = np.zeros(shape, dtype=bool)

    for i, row in enumerate(state):
        for j, seat in enumerate(row):
            if not is_seat[i, j]:
                continue

            occupied = int(state[i - 1, j - 1]) + int(state[i - 1, j]) + int(state[i - 1, j + 1]) + int(state[i, j - 1]) + int(state[
                i, j + 1]) + int(state[i + 1, j - 1]) + int(state[i + 1, j]) + int(state[i + 1, j + 1])
            if (occupied == 0 and not state[i,j]) or (occupied >= 4 and state[i,j]):
                swap[i][j] = True

    new_state = np.bitwise_xor(swap, state)
    return new_state, np.sum(swap) != 0


def print_state(state):
    print()
    for i, row in enumerate(state):
        for j, seat in enumerate(row):
            print("." if not is_seat[i, j] else ("#" if seat else "L"), end="")
        print()
    print()


changed = True
while changed:
    state, changed = find_next_state(state)

print_state(state)
print(np.sum(state))
