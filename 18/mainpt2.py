with open("input.txt", "r") as f:
    equations = f.read().strip().split("\n")

total_sum = 0


class Node:
    def __init__(self, value, parent=None, left_child=None, right_child=None):
        self.value = value
        self.parent = parent
        self.left = left_child
        self.right = right_child
        self.precedence = get_precedence(value)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        left = id(self.left) if self.left else ""
        right = id(self.right) if self.right else ""
        parent = id(self.parent) if self.parent else ""
        return f"V: {self.value} id: {id(self)} R: {right} L: {left} P: {parent}"

    def has_parent(self):
        return self.parent is not None


def get_precedence(value):
    if value == "*":
        return 2
    if value == "+":
        return 3
    if type(value) is int:
        return 4
    if value == "(":
        return 0
    if value == ")":
        return None
    else:
        raise NotImplementedError("Operation unimplemented")


def swap_with_parent(node):
    parent = node.parent
    grandparent = parent.parent
    if grandparent:
        if grandparent.left == parent:
            grandparent.left = node
        elif grandparent.right == parent:
            grandparent.right = node
        else:
            raise RuntimeError("Node's grandparent doesn't have parent as child")
    if node == parent.left:
        parent.left, parent.right, node.left, node.right = node.left, node.right, parent, parent.right
    elif node == parent.right:
        parent.left, parent.right, node.left, node.right = node.left, node.right, parent.left, parent
    else:
        raise RuntimeError("Node's parent doesn't have it as a child.")


def pop_node(node):
    if node.left is not None:
        raise RuntimeError("Can't pop")

    if node.parent:
        if node.parent.left == node:
            node.parent.left = node.right
        elif node.parent.right == node:
            node.parent.right = node.right
        else:
            raise RuntimeError("parent doesn't have current as child")

    node.right.parent = node.parent


def insert_node(parent, new):
    new.left = parent.right
    parent.right = new
    new.parent = parent


def make_tree(eq):
    root = Node("(")
    active = root

    for element in eq:
        if element == ")":
            opening = active.parent
            while opening.value != "(":
                opening = opening.parent
                if opening is None:
                    # print(active)
                    raise NotImplementedError("couldn't find matching bracket")
            pop_node(opening)
            active = opening.parent
        else:
            new = Node(element)
            while element != "(" and active and active.precedence >= new.precedence:
                active = active.parent
            insert_node(active, new)
            active = new
        # print(active)
        # pretty_print_tree(root)

    return root.right  # since we don't want to include the bracket


def pretty_print_tree(root):
    stack = [("", root)]
    print("Tree.")
    while stack:
        prefix, cur = stack.pop()

        if cur != root:
            print(prefix + "\u21B3" + " " * 5, end="")
        while True:
            print(cur.value, end="")

            if cur != root:
                prefix += " " if cur.parent.left else " "
                prefix += " " * (len(str(cur.value)) + 4)

            if cur.left:
                stack.append((prefix, cur.left))

            cur = cur.right
            if cur is None:
                print()
                break
            print(end=" --> ")
    print("End tree.")


def pre_parse(eq):
    parsed_eq = []
    cur_value = []
    for c in eq:
        if len(cur_value) != 0:
            if c.isnumeric():
                cur_value.append(c)
                continue
            else:
                parsed_eq.append(int("".join(cur_value)))
                cur_value = []
        if c == " ":
            continue
        elif c.isnumeric():
            cur_value.append(c)
        else:
            parsed_eq.append(c)

    if cur_value:
        parsed_eq.append(int("".join(cur_value)))

    return parsed_eq


def evaluate(node):
    if type(node.value) != str:
        return node.value
    elif node.value == "*":
        return evaluate(node.left) * evaluate(node.right)
    elif node.value == "+":
        return evaluate(node.left) + evaluate(node.right)
    else:
        raise NotImplementedError(f"Operation {node.value} not supported")


for equation in equations:
    pre_parsed = pre_parse(equation)
    # print(pre_parsed)
    tree = make_tree(pre_parsed)
    # pretty_print_tree(tree)
    ans = evaluate(tree)
    print(ans)
    total_sum += ans

print()
print(total_sum)
