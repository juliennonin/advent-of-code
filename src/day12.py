# %%
import numpy as np

#%%
def parser(filename):
    with open(filename) as f:
        data = [(instr[0], int(instr[1:])) for instr in f.read().splitlines()]
    return data

# %%
def travel(instructions):
    dir_vector = {"E" : np.array([1, 0]), "S": np.array([0, -1]), "W": np.array([-1, 0]), "N": np.array([0, 1])}
    dirs = "ESWN"
    
    dir = 0  # current direction idx
    pos = np.array([0, 0])  # current position

    for instr, value in instructions:
        if instr == "F":
            pos += value * dir_vector[dirs[dir]]
        elif instr in dirs:
            pos += value * dir_vector[instr]
        elif instr in "RL":
            sign = 1 if instr == "R" else -1
            dir = (dir + sign * value//90) % len(dirs)

    return pos

# %%
def travel_with_waypoint(instructions):
    dir_vector = {"E" : np.array([1, 0]), "S": np.array([0, -1]), "W": np.array([-1, 0]), "N": np.array([0, 1])}
    rotation = lambda theta: np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]], dtype=int)
    dirs = "ESWN"

    pos = np.array([0, 0], dtype=int)  # current position
    wpt = np.array([10, 1], dtype=int)  # current waypoint position

    for instr, value in instructions:
        if instr == "F":  # move 'value' times forward to the waypoint
            pos += value * wpt
        elif instr in dirs:  # move the waypoint to E/S/W/N by the given value
            wpt += value * dir_vector[instr]
        elif instr in "RL":  # rotate the waypoint to R/L by the given value (degree)
            sign = 1 if instr == "R" else -1
            wpt = wpt @ rotation(np.deg2rad(sign * value))

    return pos

# %%
if __name__ == "__main__":
    from os.path import dirname, join, realpath, basename
    folder = join(dirname(dirname(realpath(__file__))), "data")
    instructions = parser(f"{folder}/day12.txt")

    print("Part 1 —", np.abs(travel(instructions)).sum())
    print("Part 2 —", np.abs(travel_with_waypoint(instructions)).sum())
