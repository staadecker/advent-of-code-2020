def main():
    with open("input.txt", "r") as f:
        rules_raw = f.readlines()

    graph = {}

    for rule in rules_raw:
        (outer_bag, inner_bags) = parse_rule(rule)

        if inner_bags is None:
            continue

        graph[outer_bag] = inner_bags

    stack = [(1, "shiny gold")]
    sub_bags = 0

    while len(stack) > 0:
        (multiplier, node) = stack.pop()

        for edge in graph[node]:
            new_multiplier = edge[0] * multiplier
            sub_bags += new_multiplier
            if edge[1] in graph:
                stack.append((new_multiplier, edge[1]))

    print(sub_bags)


def parse_rule(rule):
    [outer_bag, inner_bags_raw] = rule.split(" bags contain ")

    if inner_bags_raw.find("no other bags.") != -1:
        return None, None

    inner_bags = []

    for inner_bag_raw in inner_bags_raw.split(", "):
        # Remove number and suffix
        inner_bag = inner_bag_raw[:inner_bag_raw.find("bag") - 1]
        (count, name) = inner_bag.split(" ", 1)

        inner_bags.append((int(count), name))

    return outer_bag, inner_bags


if __name__ == "__main__":
    main()
