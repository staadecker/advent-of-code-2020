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

            occupied = 0

            # scan up
            for x in range(i - 1, 0, -1):
                if is_seat[x, j]:
                    occupied += int(state[x, j])
                    break

            # scan down
            for x in range(i + 1, len(seats)):
                if is_seat[x, j]:
                    occupied += int(state[x, j])
                    break

            # scan left
            for y in range(j - 1, 0, -1):
                if is_seat[i, y]:
                    occupied += int(state[i, y])
                    break

            # scan right
            for y in range(j + 1, len(row)):
                if is_seat[i, y]:
                    occupied += int(state[i, y])
                    break

            # scan up_right
            for offset in range(1, min(i, len(row) - j)):
                pos = i - offset, j + offset
                if is_seat[pos]:
                    occupied += int(state[pos])
                    break

            # scan up_left
            for offset in range(1, min(i, j)):
                pos = i - offset, j - offset
                if is_seat[pos]:
                    occupied += int(state[pos])
                    break

            # scan down_right
            for offset in range(1, min(len(seats) - i, len(row) - j)):
                pos = i + offset, j + offset
                if is_seat[pos]:
                    occupied += int(state[pos])
                    break

            # scan down_left
            for offset in range(1, min(len(seats) - i, j)):
                pos = i + offset, j - offset
                if is_seat[pos]:
                    occupied += int(state[pos])
                    break

            if (occupied == 0 and not state[i, j]) or (occupied >= 5 and state[i, j]):
                swap[i][j] = True

    new_state = np.bitwise_xor(swap, state)
    return new_state, np.sum(swap) != 0


def print_state(state):
    print()
    for i, row in enumerate(state):
        if i == 0 or i == len(state) - 1:
            continue
        for j, seat in enumerate(row):
            if j == 0 or j == len(row) - 1:
                continue
            print("." if not is_seat[i, j] else ("#" if seat else "L"), end="")
        print()
    print()


changed = True
while changed:
    print_state(state)
    state, changed = find_next_state(state)

print_state(state)
print(np.sum(state))
