with open("input.txt","r") as f:
    d = f.readlines()

d = list(map(lambda row: row.strip(), d))

def find_trees(slope_x, slope_y):
    x = slope_x
    y = slope_y

    width = len(d[0])

    trees = 0

    print(d[0])
    print(width)

    while y < len(d):
        
        if d[y][x % width] == "#":
            trees+=1
        x += slope_x
        y += slope_y

    return trees
print(find_trees(1,1) * find_trees(3,1) * find_trees(5,1) * find_trees(7,1) * find_trees(1,2))
