JUMP = "jmp"
ACCUMULATE = "acc"
NOP = "nop"

instruction_mapping = {"jmp": JUMP, "acc": ACCUMULATE, "nop": NOP}


def main():
    instructions = parse_input("input.txt")
    visited = [0] * len(instructions)
    accumulator = [-1] * len(instructions)

    previous_switch = -1
    next_line = 0
    section = 1
    prev_accumulator = 0

    while True:
        (accumulator, visited, prev_accumulator, isEnd) = explore_section(instructions, accumulator, visited,
                                                                          prev_accumulator, next_line,
                                                                          section)
        if isEnd:
            print(prev_accumulator)
            break

        (previous_switch, next_line, prev_accumulator) = find_next_switch(instructions, previous_switch, visited, accumulator)
        section += 1


def find_next_switch(instructions, previous_switch, visited, accumulators):
    next_switch = previous_switch + 1
    while next_switch < len(instructions):
        instruction_code = instructions[next_switch][0]
        if visited[next_switch] == 1 and (instruction_code == JUMP or instruction_code == NOP):
            (next_line, accumulator) = run_instruction(switch_instruction(instructions[next_switch]),
                                                       next_switch, accumulators[next_switch])
            if visited[next_line] == 0:
                return next_switch, next_line, accumulator

        next_switch += 1

    raise RuntimeError("No solution found.")


def switch_instruction(instruction):
    if instruction[0] == JUMP:
        return NOP, instruction[1]
    if instruction[0] == NOP:
        return JUMP, instruction[1]
    raise RuntimeError("instruction not switchable")


def explore_section(instructions, accumulator, visited, curr_accumulator, next_line, section):
    # while section unexplored
    while next_line < len(instructions) and visited[next_line] == 0:
        curr_line = next_line

        (next_line, curr_accumulator) = run_instruction(instructions[curr_line], curr_line, curr_accumulator)

        visited[curr_line] = section  # mark as visited
        accumulator[curr_line] = curr_accumulator

    return accumulator, visited, curr_accumulator, next_line == len(instructions)


def run_instruction(instruction, current_line, prev_accumulator):
    (instruction_code, operand) = instruction

    # Run instruction
    if instruction_code == JUMP:
        return current_line + operand, prev_accumulator
    if instruction_code == ACCUMULATE:
        return current_line + 1, prev_accumulator + operand
    if instruction_code == NOP:
        return current_line + 1, prev_accumulator

    raise RuntimeError("Unknown operation.")


def parse_input(filename):
    instructions = []

    with open(filename, "r") as f:
        data = f.readlines()

    for row in data:
        [instruction, operand] = row.split(" ")
        instructions.append((instruction, int(operand)))

    return instructions


if __name__ == "__main__":
    main()
