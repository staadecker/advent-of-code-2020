with open("input.txt", "r") as f:
    instructions = f.readlines()


def make_mask(instruction):
    or_mask = 0
    and_mask = 0
    for bit in instruction[7:].strip():
        or_mask = or_mask << 1
        and_mask = and_mask << 1
        if bit == "X":
            and_mask += 1
        elif bit == "0":
            pass
        elif bit == "1":
            or_mask += 1
            and_mask += 1
        else:
            raise RuntimeError("Invalid mask")
    return or_mask, and_mask


def apply_mask(value, masks):
    return (value & masks[1]) | masks[0]


memory = {}
current_mask = (0, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)

for instruction in instructions:
    if instruction[0:4] == "mask":
        current_mask = make_mask(instruction)
    else:
        address = int(instruction[4:instruction.index("]")])
        value = int(instruction[instruction.index("=") + 1:])
        memory[address] = apply_mask(value, current_mask)

print(memory)
print(sum(memory.values()))
