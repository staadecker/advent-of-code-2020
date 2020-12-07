visited = "visited"
edges = "edges"


def main():
    with open("input.txt", "r") as f:
        rules_raw = f.readlines()

    graph = {}
    canReach = {}

    for rule in rules_raw:
        (outer_bag, inner_bags) = parse_rule(rule)

        if inner_bags is None:
            continue

        if outer_bag not in graph:
            graph[outer_bag] = {visited: False, edges: []}

        for inner_bag in inner_bags:
            if inner_bag not in graph:
                graph[inner_bag] = {visited: False, edges: [outer_bag]}
            else:
                graph[inner_bag]["edges"].append(outer_bag)

    stack = ["shiny gold"]

    while len(stack) > 0:
        node = stack.pop()
        graph[node][visited] = True

        for edge in graph[node][edges]:
            if not graph[edge][visited]:
                stack.append(edge)

    visited_count = -1  # -1 since the current bag although visited doesn't count
    for node in graph.values():
        if node[visited]:
            visited_count += 1
    print(visited_count)


def parse_rule(rule):
    [outer_bag, inner_bags_raw] = rule.split(" bags contain ")

    if inner_bags_raw == "no other bags.\n":
        return None, None

    inner_bags = []

    for inner_bag_raw in inner_bags_raw.split(", "):
        # Remove number and suffix
        inner_bags.append(inner_bag_raw[2:inner_bag_raw.find("bag") - 1])

    return outer_bag, inner_bags


if __name__ == "__main__":
    main()
