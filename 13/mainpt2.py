with open("input.txt", "r") as f:
    unordered_bus = f.readlines()[1].split(",")

buses = []

for i, bus in enumerate(unordered_bus):
    if bus == "x":
        continue

    buses.append((int(bus), i))

buses = sorted(buses, key=lambda x: x[0], reverse=True)

print(buses)

timestamp = 0
increment = 1

for (id, offset) in buses:
    while True:
        if (timestamp + offset) % id == 0:
            break
        timestamp += increment

    increment *= id


print(timestamp)
