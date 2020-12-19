with open("inputv2.txt", "r") as f:
    rules, messages = f.read().split("\n\n")


def parse_rules(rule_str):
    rule_str = rule_str.strip().split("\n")

    rules = {}

    for rule in rule_str:
        rule_id, match1 = rule.split(": ")

        rule_id = int(rule_id)

        if match1.find("|") != -1:
            match1, match2 = match1.split(" | ")
        else:
            match2 = None
        if match1[0] == '"':
            rules[rule_id] = match1[1:-1]
            continue

        match1 = list(map(int, match1.strip().split(" ")))
        matches = [match1]
        if match2:
            match2 = list(map(int, match2.strip().split(" ")))
            matches.append(match2)

        rules[rule_id] = matches

    return rules


def parse_messages(messages):
    return messages.strip().split("\n")


rules = parse_rules(rules)
messages = parse_messages(messages)
evaluated_rules = {}


def get_matches(rule, parent_id):
    answers = []
    evaluate = True
    for sub_rule in rule:
        if sub_rule == parent_id:
            evaluate = False
            continue
        sub_rule_values = evaluate_rule(sub_rule)
        if sub_rule_values is None:
            evaluate = False
            continue
        if not answers:
            answers = sub_rule_values
            continue

        build_answers = set()

        for sub_rule_values in sub_rule_values:
            for cur_answer in answers:
                build_answers.add(cur_answer + sub_rule_values)

        answers = build_answers
    return answers if evaluate else None


def evaluate_rule(rule_id):
    if rule_id in evaluated_rules:
        return evaluated_rules[rule_id]
    if type(rules[rule_id]) == str:
        return set(rules[rule_id])
    all_matches = set()
    for rule in rules[rule_id]:
        matches = get_matches(rule, rule_id)

        if matches is None:
            all_matches = None
            break

        all_matches = all_matches.union(matches)

    evaluated_rules[rule_id] = all_matches
    return all_matches


options = evaluate_rule(0)
# options31 = evaluate_rule(31)


# print(options[0])
# print(options31)
print(rules[0])
print(rules[8])
print(rules[11])
print(evaluated_rules[42])
print(evaluated_rules[31])


def is_message_valid(message, chunk_size):
    chunks = []
    for i in range(0, len(message), chunk_size):
        chunks.append(message[i:i + chunk_size])

    max_number_of_31 = 1

    while chunks[-max_number_of_31] in evaluated_rules[31] and max_number_of_31 < len(chunks):
        max_number_of_31 += 1
    max_number_of_31 -= 1

    if max_number_of_31 == 0:
        return False

    for i, chunk in enumerate(chunks):
        if chunk not in evaluated_rules[42]:
            return False
        if i + 1 >= len(chunks) - max_number_of_31 and i >= max_number_of_31:
            return True

    return False


def verify_messages(messages):
    valid = 0
    invalid = 0
    chunk_size = len(next(iter(evaluated_rules[42]))) # Retrieve length of an element in set
    for message in messages:
        if is_message_valid(message, chunk_size):
            valid += 1
        else:
            invalid += 1

    return valid, invalid


print(verify_messages(messages))
