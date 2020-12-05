# %%
from math import log2

# %%
def get_position_and_id(seat, n=128, m=8):
    k = int(log2(n))  # 7 for default n = 128
    bin_row = seat[:k].replace('F', '0').replace('B', '1')
    bin_col= seat[k:].replace('L', '0').replace('R', '1')
    i, j = int(bin_row, 2), int(bin_col, 2)
    return i, j, i * m + j

# %%
def find_my_seat(passes, n=128, m=8):
    seats = [0] * (n * m)
    id_min, id_max = n * m ,0
    for seat in passes:
        i, j, id = get_position_and_id(seat)
        if id < id_min: id_min = id
        elif id > id_max: id_max = id
        seats[id] += 1
    # seats is of the form [0,0,...,0,1,1,...1,1,0,1,1,...,1,1,0,0,...,0]
    #                                 ↑          ↑           ↑
    #                               id_min     my_id       id_max
    return id_min + seats[id_min:id_max+1].index(0)

# %%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")
    
    with open(f"{folder}/day5.txt") as f:
        passes = f.read().splitlines()

    print("Part 1 —", max(get_position_and_id(seat)[2] for seat in passes))
    print("Part 2 —", find_my_seat(passes))

# %%
