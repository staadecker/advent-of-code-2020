import math

with open("input.txt", "r") as f:
    instructions = list(map(lambda s: (s[0].strip(), int(s[1:])), f.readlines()))

x = 0
y = 0
dir = 0

for (instruction, amount) in instructions:
    if instruction == "N":
        y += amount
    elif instruction == "S":
        y -= amount
    elif instruction == "E":
        x += amount
    elif instruction == "W":
        x -= amount
    elif instruction == "L":
        dir += amount
    elif instruction == "R":
        dir -= amount
    elif instruction == "F":
        x += amount * math.cos(dir / 180 * math.pi)
        y += amount * math.sin(dir / 180 * math.pi)
    else:
        print(instruction)
        raise IOError("Invalid instruction")
    # print(instruction, amount, x,y)

print(x, y, abs(x)+abs(y))