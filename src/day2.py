# %%
def parser(line):
    a, b, letter, pwd = line.replace('-', ' ').replace(':', '').split(' ')
    return int(a), int(b), letter, pwd

# %% Part 1
def pwd_checker_sled(min_occ, max_occ, letter, pwd):
    return min_occ <= pwd.count(letter) <= max_occ

# %% Part 2
def pwd_checker_toboggan(pos1, pos2, letter, pwd):
    return (pwd[pos1-1] == letter) != (pwd[pos2-1] == letter)  # XOR

# %%
if __name__ == '__main__':
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")
    with open(f"{folder}/day2.txt") as f:
        data = f.read().splitlines()
    print("Part 1 —", sum(pwd_checker_sled(*parser(line)) for line in data))
    print("Part 2 —", sum(pwd_checker_toboggan(*parser(line)) for line in data))

# %%
