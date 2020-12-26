def main(filename):
    ingredients, allergens = read_input(filename)
    print(ingredients, allergens)
    possibilities = find_possibilities(ingredients, allergens)
    print(possibilities)
    allergen_free = find_allergen_free_ingredients(ingredients, possibilities)
    print(allergen_free)
    count = count_allergen_free(ingredients, allergen_free)
    print(count)
    allergen_ingredients = get_allergen_only_ingredients(ingredients, allergen_free)
    possibilities = find_possibilities(allergen_ingredients, allergens)
    print(allergen_ingredients)
    print([len(row) for row in allergen_ingredients])
    print([len(row) for row in allergens])
    print(possibilities)
    solution = find_allergens(allergen_ingredients, allergens)
    print(format_solution(solution))


def read_input(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
    ingredients = []
    allergens = []
    for line in lines:
        ingredient = line[:line.index("(")].strip()
        ingredients.append(set(ingredient.split(" ")))
        allergen = line[line.index("contains ") + 9:-1]
        allergens.append(set(allergen.split(", ")))

    return ingredients, allergens


def find_possibilities(ingredients, allergens):
    possibilities = {}
    for i, allergen_row in enumerate(allergens):
        for allergen in allergen_row:
            if allergen not in possibilities:
                possibilities[allergen] = ingredients[i]
            else:
                possibilities[allergen] = possibilities[allergen].intersection(ingredients[i])
    return possibilities


def find_allergen_free_ingredients(ingredients, possibilities):
    allergen_ingredients = set()
    for possibility in possibilities.values():
        allergen_ingredients = allergen_ingredients.union(possibility)

    all_ingredients = set()
    for ingredient_row in ingredients:
        all_ingredients = all_ingredients.union(ingredient_row)

    return all_ingredients.difference(allergen_ingredients)


def count_allergen_free(ingredients, allergen_free):
    count = 0
    for search_ingredient in allergen_free:
        for ingredient_row in ingredients:
            if search_ingredient in ingredient_row:
                count += 1
    return count


def get_allergen_only_ingredients(ingredients, allergen_free):
    allergen_ingredients = []
    for ingredient_row in ingredients:
        allergen_ingredients.append(ingredient_row.difference(allergen_free))

    return allergen_ingredients


def find_allergens(ingredients, allergens):
    found_allergens_map = {}
    found_allergens = set()
    possibilities = find_possibilities(ingredients, allergens)
    while len(possibilities) > 0:
        for allergen, possibility in possibilities.items():
            if len(possibility) == 1:
                found_allergens_map[allergen] = list(possibility)[0]
                found_allergens.add(allergen)
                possibilities.pop(allergen)
                for key in possibilities.keys():
                    possibilities[key] = possibilities[key].difference(possibility)
                break

    return found_allergens_map

def format_solution(solution):
    sorted_solution = list(sorted(solution.items(), key=lambda key_value: key_value[0]))
    formatted = ",".join(list(map(lambda x: x[1], sorted_solution)))
    return formatted

if __name__ == '__main__':
    filename = "input.txt"
    main(filename)
