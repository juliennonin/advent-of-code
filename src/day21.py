# %%
import re

# %%
def parser(filename):

    with open(filename) as f:
        data = f.read().splitlines()

    all_to_ingr = {}  # allergene -> potential ingredients
    receipes = []  # list of (ingredients, allergenes)
    for line in data:
        ingredients, allergenes = re.match("(.*) \(contains (.*)\)", line).groups()
        ingredients, allergenes = ingredients.split(' '), allergenes.split(', ')
        receipes.append((ingredients, allergenes))

        for allergene in allergenes:
            s = all_to_ingr.setdefault(allergene, set(ingredients))
            all_to_ingr[allergene] = s.intersection(ingredients)

    ingr_to_all = {}  # ingredient -> potential allergenes
    for allergene, ingredients in all_to_ingr.items():
        for ingr in ingredients:
            ingr_to_all.setdefault(ingr, set()).add(allergene)
    
    return receipes, all_to_ingr, ingr_to_all

#%%
def infer_allergenes(all_to_ingr, ingr_to_all):
    all_to_check = [al for al in all_to_ingr if len(all_to_ingr[al]) == 1]
    dangerous_ingrs = {}  # ingredient -> allergene

    while len(all_to_check) > 0:
        allergene = all_to_check.pop(0)
        if allergene in dangerous_ingrs.values(): continue  # allergene already checked

        ingredients = all_to_ingr[allergene] - dangerous_ingrs.keys()
        # If there is only one ingredient left for this allergene, we have found the allergene - ingredient pair !
        if len(ingredients) == 1:
            ingr, = ingredients
            dangerous_ingrs[ingr] = allergene

            # visit other potential allerges (that are actually not the allergene of this ingredient)
            for al in ingr_to_all[ingr]:
                all_to_check.append(al)

    return dangerous_ingrs


# %%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")    
    receipes, all_to_ingr, ingr_to_all = parser(f"{folder}/day21.txt")

    safe_ingrs = {}
    for food, _ in receipes:
        for ingr in food:
            if not ingr in ingr_to_all:
                safe_ingrs[ingr] = safe_ingrs.get(ingr, 0) + 1
    print("Part 1 —", sum(safe_ingrs.values()))

    dangerous_ingrs = infer_allergenes(all_to_ingr, ingr_to_all)
    print("Part 2 —",','.join(sorted(dangerous_ingrs, key=lambda ingr: dangerous_ingrs[ingr])))

