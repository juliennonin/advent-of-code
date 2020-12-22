# %%
from functools import reduce

# %%
def count_any(group):
    return len(set(group.replace("\n", "")))


def count_every(group):
    intersection = lambda x,y: set(x).intersection(y)
    return len(reduce(intersection, group.split('\n')))

# %%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")
    
    with open(f"{folder}/day06.txt") as f:
        data = f.read().split("\n\n")
    
    print("Part 1 —", sum(count_any(group) for group in data))
    print("Part 2 —", sum(count_every(group) for group in data))