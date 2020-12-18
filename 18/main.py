ADD = 0
MUL = 1

with open("input.txt", "r") as f:
    equations = f.read().strip().split("\n")


def find_matching_bracket(eq, i):
    j = i
    inner_brackets = 0
    outer_brackets = 0
    while True:
        if eq[j] == ")":
            outer_brackets += 1
            if outer_brackets == inner_brackets + 1:
                return j
        elif eq[j] == "(":
            inner_brackets += 1
        j += 1


def apply_op(running_total, value, op):
    if op == MUL:
        return running_total * value
    if op == ADD:
        return running_total + value


def solve_equation(eq):
    running_total = 0
    cur_op = ADD
    i = 0
    while i < len(eq):
        if eq[i] == " ":
            pass
        elif eq[i] == "(":
            j = find_matching_bracket(eq, i+1)
            running_total = apply_op(running_total, solve_equation(eq[i + 1:j]), cur_op)
            i = j
        elif eq[i] == "*":
            cur_op = MUL
        elif eq[i] == "+":
            cur_op = ADD
        else:
            j = i + 1
            while j < len(eq) and eq[j].isnumeric():
                j += 1
            running_total = apply_op(running_total, int("".join(eq[i:j])), cur_op)
            i = j - 1
        i += 1

    return running_total


total_sum = 0
for equation in equations:
    ans = solve_equation(list(equation))
    # print(ans, equation)
    total_sum += ans

print(total_sum)
