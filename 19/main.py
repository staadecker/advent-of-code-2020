with open("input.txt", "r") as f:
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
evaluated_rule = {}


def evaluate_rule(rule_id):
    if rule_id in evaluated_rule:
        return evaluated_rule[rule_id]
    if type(rules[rule_id]) == str:
        return set(rules[rule_id])
    answers_for_all_matches = set()
    for option in rules[rule_id]:
        answers = evaluate_rule(option[0])
        for sub_rule in option[1:]:
            sub_rule_values = evaluate_rule(sub_rule)

            build_answers = set()

            for sub_rule_values in sub_rule_values:
                for cur_answer in answers:
                    build_answers.add(cur_answer + sub_rule_values)

            answers = build_answers
        answers_for_all_matches = answers_for_all_matches.union(answers)
    evaluated_rule[rule_id] = answers_for_all_matches
    return answers_for_all_matches


options = evaluate_rule(0)


# print(options)
# print(evaluated_rule)


def verify_messages(options, messages):
    valid = 0
    invalid = 0
    for message in messages:
        if message in options:
            valid += 1
        else:
            invalid += 1
    return valid, invalid


print(verify_messages(options, messages))
