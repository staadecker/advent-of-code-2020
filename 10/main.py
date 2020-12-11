with open("input.txt", "r") as f:
    data = sorted(list(map(lambda x: int(x), f.readlines())))
    data.insert(0, 0)

arrangements = [0] * len(data)
arrangements[0] = 1

for i, data_point in enumerate(data):
    if i == 0:
        continue

    value = 0
    if i - 1 >=0:
        value += arrangements[i-1]
    if i - 2 >= 0 and data_point - data[i-2] <= 3:
        value += arrangements[i-2]
    if i - 3 >= 0 and data_point - data[i-3] <= 3:
        value += arrangements[i-3]

    arrangements[i] = value

print(data)
print(arrangements)
