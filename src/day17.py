#%%
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

# %%
def parser(filename):
    with open(filename) as f:
        data = [[0 if s=='.' else 1 for s in line] for line in f.read().splitlines()]
    return data

# %%
def apply_conway_n_times(A, n):
    dim = A.ndim  # dimension
    Z = np.pad(A, (1 + n))  # add enough border
    N = np.zeros(Z.shape, dtype=int)  # number of neighbors
    center = (np.s_[1:-1],) * dim  # core of the grid (no borders)
    
    for _ in range(n):
        # Compute the number of neighbors
        N[...] = 0
        for neigh_slice in product([np.s_[:-2], np.s_[1:-1], np.s_[2:]], repeat=dim):
            if neigh_slice != center:
                N[center] += Z[neigh_slice]

        # Update the Conway grid
        birth = (N == 3) & (Z == 0)  # inactive cell with 3 neighbors becomes active
        survive = ((N == 2) | (N == 3)) & (Z == 1)  # active cell with 2 or 3 neig. stays active
        Z[...] = 0
        Z[birth | survive] = 1
    
    return Z

# %%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")
    data = parser(f"{folder}/day17.txt")
    n = len(data)
    
    Z_3d = np.zeros((n,)*3, dtype=int)
    Z_3d[n//2] = data

    Z_4d = np.zeros((n,)*4, dtype=int)
    Z_4d[n//2, n//2] = data

    print("Part 1 —", apply_conway_n_times(Z_3d, 6).sum())
    print("Part 2 —", apply_conway_n_times(Z_4d, 6).sum())

