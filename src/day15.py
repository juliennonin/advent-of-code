#%%
def memory_game(init, N):
    first_round = len(init)
    n = init.pop()
    d = {m: i+1 for i, m in enumerate(init)}

    for round in range(first_round, N):
        new = round - d.get(n, round)
        d[n], n = round, new
    
    return n

# %%
if __name__ == "__main__":
    from os.path import dirname, join, realpath, basename
    folder = join(dirname(dirname(realpath(__file__))), "data")
    with open(f"{folder}/day15.txt") as f:
        data = list(map(int, f.read().split(',')))

    print("Part 1 —", memory_game(data, 2020))
    print("Part 2 —", memory_game(data, 30000000))
# %%
