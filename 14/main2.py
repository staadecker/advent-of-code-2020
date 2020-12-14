with open("input.txt", "r") as f:
    instructions = f.readlines()


def get_addresses(root_address, mask):
    if mask is None:
        return [root_address]
    addresses = [0]
    pos_mask = 0x800000000
    pos_index = 0
    while pos_mask != 0:
        mask_bit = mask[pos_index]
        root_bit = root_address & pos_mask != 0
        for i in range(len(addresses)):
            addresses[i] = addresses[i] << 1
            if mask_bit == "1":
                addresses[i] += 1
            if mask_bit == "X":
                addresses.append(addresses[i] + 1)
            if mask_bit == "0":
                addresses[i] += root_bit
        pos_mask = pos_mask >> 1
        pos_index += 1
    return addresses




memory = {}
current_mask = None

for instruction in instructions:
    if instruction[0:4] == "mask":
        current_mask = instruction[7:].strip()
    else:
        address = int(instruction[4:instruction.index("]")])
        value = int(instruction[instruction.index("=") + 1:])
        for a in get_addresses(address, current_mask):
            memory[a] = value

print(memory)
print(sum(memory.values()))
