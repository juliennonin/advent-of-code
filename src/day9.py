#%%
from day1 import find_two_entries_that_sum_to_N

# %%
def find_not_sum_of_N_previous_numbers(data, N):
    for i in range(0, len(data) - N):
        if not find_two_entries_that_sum_to_N(data[i:N+i], data[N+i]):
            return data[N+i]

# %%
def find_continuous_subset_that_sums_to_k(data, k):
    for i in range(len(data)):
        s, j = 0, 0
        while s < k:
            s += data[i+j]
            j += 1
        if s == k:
            subset = data[i:i+j]
            return subset

# %%
if __name__ == '__main__':
    from os.path import dirname, join, realpath
    from numpy import loadtxt
    folder = join(dirname(dirname(realpath(__file__))), "data")
    
    N = 25
    data = loadtxt(f"{folder}/day9.txt", dtype=int)
    weakness = find_not_sum_of_N_previous_numbers(data, N)
    subset = find_continuous_subset_that_sums_to_k(data, weakness)
    
    print("Part 1 —", weakness)
    print("Part 2 —", min(subset) + max(subset))

