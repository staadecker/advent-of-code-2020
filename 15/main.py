with open("input.txt", "r") as file:
    numbers = file.read().strip().split(",")

data = {}

index = 1  # start at 1 to match question
previous = None

for number in numbers:
    if previous is not None:
        data[previous] = index - 1
    previous = int(number)
    index += 1

while index <= 30000000:
    number = (index - 1 - data[previous]) if previous in data else 0
    data[previous] = index - 1
    previous = number
    index += 1

print(previous)
