# %%
from functools import reduce

# %%
def slope(right, down, height, width):
    i, j = 0, 0
    while i < height:
        yield i, j
        i += down
        j += right
        j %= width

# %%
def nb_of_trees_in_multiple_slopes(mmap, slopes):
    n, m = len(mmap), len(mmap[0])
    nb_trees = []
    for sl in slopes:
        obj_encountered = [mmap[x][y] for x, y in slope(*sl, n, m)]
        nb_trees.append(obj_encountered.count("#"))
    return nb_trees

def prod(L):
    return reduce(lambda x, y: x * y, L)

# %%
if __name__ == '__main__':
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")
    with open(f"{folder}/day03.txt") as f:
        M = f.read().splitlines()
    
    print("Part 1 —", *nb_of_trees_in_multiple_slopes(M, [(3, 1)]))
    print("Part 2 —", prod(nb_of_trees_in_multiple_slopes(M, [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])))

# %%
