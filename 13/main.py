import math

with open("input.txt", "r") as f:
    (arrival, buses) = f.readlines()

arrival = int(arrival)
buses = map(lambda x: int(x), filter(lambda x: x != "x", buses.split(",")))

favourite_bus = (None, math.inf)
for bus in buses:

    wait_time = bus * ((arrival // bus) + 1) - arrival
    if wait_time < favourite_bus[1]:
        favourite_bus = (bus, wait_time)

print(favourite_bus[0] * favourite_bus[1])
