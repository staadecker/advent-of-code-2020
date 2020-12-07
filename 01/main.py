with open("input.txt", "r") as f:
    values = f.readlines()

    values = list(map(lambda x: int(x), values))

    print(values)
    for value in values:
        v2 = 2020 - value
        for v3 in values:
            if v2 - v3 in values:
                print(value)
