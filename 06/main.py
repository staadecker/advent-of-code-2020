with open("input.txt","r") as f:
    data = f.read().split("\n\n")

total = 0

for group in data:
    people = group.split("\n")

    everyone = 0

    for char in people[0]:
        allTrue = True
        for person in people[1:]:
            if person != '' and person.find(char) == -1:
                allTrue = False
        if allTrue:
            everyone +=1
    print(everyone)
    total += everyone

print(total)
