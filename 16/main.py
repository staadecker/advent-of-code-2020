# Disclaimer: This code is an absolute mess, it works but will be impossible to understand so don't bother.
# The reason I'm ok with it being a mess is that it only needs to work once and now that I'm done the challenge
# No one ever needs to look at it again

with open("input.txt", "r") as file:
    rules_raw, my_ticket, nearby_tickets = file.read().split("\n\n")

my_ticket = list(map(int, my_ticket.split("\n")[1].strip().split(",")))
nearby_tickets = list(map(lambda x: list(map(int, x.split(","))), nearby_tickets.strip().split("\n")[1:]))
is_valid_ticket = [True] * len(nearby_tickets)

fields = []
answer = []
rules = []


class Range:
    def __init__(self, range):
        self.range = tuple(map(int, range.split("-")))

    def in_range(self, value):
        return self.range[0] <= value <= self.range[1]

    def __repr__(self):
        return str(self.range)


for rule in rules_raw.split("\n"):
    (field, ranges) = rule.split(": ")
    fields.append(field)
    rules.append(tuple(map(Range, ranges.split(" or "))))

# Find invalid tickets
for i, nearby_ticket in enumerate(nearby_tickets):
    for j, number in enumerate(nearby_ticket):
        invalid = True
        for rule in rules:
            if rule[0].in_range(number) or rule[1].in_range(number):
                invalid = False
                break
        if invalid:
            is_valid_ticket[i] = False
            break

valid_tickets = [my_ticket]
for i in range(len(nearby_tickets)):
    if is_valid_ticket[i]:
        valid_tickets.append(nearby_tickets[i])

answer = [[True] * len(fields) for _ in range(len(my_ticket))]
possibilities = [len(fields)] * len(my_ticket)
final_answer = [None] * len(my_ticket)
fields_remaining = len(final_answer)

while fields_remaining > 0:
    for valid_ticket in valid_tickets:
        for i, number in enumerate(valid_ticket):
            for j, rule in enumerate(rules):
                if answer[i][j] and not rule[0].in_range(number) and not rule[1].in_range(number):
                    answer[i][j] = False
                    possibilities[i] -= 1
            if possibilities[i] == 1:
                for k, is_answer in enumerate(answer[i]):
                    if is_answer:
                        final_answer[i] = k
                        fields_remaining-=1
                        break
                for l in range(len(my_ticket)):
                    if answer[l][k]:
                        answer[l][k] = False # Mark other slots as not being the slot we found the answer to
                        possibilities[l] -= 1

print(final_answer, possibilities, my_ticket, fields, sep="\n")

running_total = 1

for i in range(len(my_ticket)):
    field = fields[final_answer[i]]
    if field.find("departure") != -1:
        running_total = my_ticket[i] * running_total
        print(field, my_ticket[i], sep=": ", end=", ")

print(running_total)