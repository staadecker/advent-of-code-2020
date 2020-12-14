import math

with open("input.txt", "r") as f:
    instructions = list(map(lambda s: (s[0].strip(), int(s[1:])), f.readlines()))

w_x = 10
w_y = 1
s_x = 0
s_y = 0
dir = 0

for (instruction, amount) in instructions:
    if instruction in ("S", "W", "R"):
        amount = -amount
    if instruction in ("N", "S"):
        w_y += amount
    elif instruction in ("E", "W"):
        w_x += amount
    elif instruction in ("L", "R"):
        angle = amount / 180 * math.pi
        w_x, w_y = w_x * math.cos(angle) - w_y * math.sin(angle), w_x * math.sin(angle) + w_y * math.cos(angle)
    elif instruction == "F":
        s_x += w_x * amount
        s_y += w_y * amount
    else:
        print(instruction)
        raise IOError("Invalid instruction")
    print(instruction, amount, w_x, w_y, s_x, s_y)

print(abs(s_y) + abs(s_x))
