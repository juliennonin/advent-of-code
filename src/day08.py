#%%
def parser(filename):
    with open(filename) as f:
        instructions = [(line[:3], int(line[4:])) for line in f.read().splitlines()]
    return instructions

#%%
def run_instructions(instructions):
    accumulator = 0
    visited = [False] * len(instructions)
    i = 0
    while i < len(instructions) and not visited[i]:
        instruction, argt = instructions[i]
        visited[i] = True
        if instruction == 'nop':
            i += 1
        elif instruction == 'acc':
            accumulator += argt
            i += 1
        elif instruction == 'jmp':
            i += argt
    return i >= len(instructions), accumulator

#%%
def small_fixes(instructions):
    change_rules = {'nop': 'jmp', 'jmp': 'nop'}
    for i, (instr, value) in enumerate(instructions):
        if instr in change_rules:
            yield instructions[:i] + [(change_rules[instr], value)] + instructions[i+1:]

def fix_instructions(instructions):
    for instructions_fixed in small_fixes(instructions):
        is_fixed, accumulator = run_instructions(instructions_fixed)
        if is_fixed:
            return accumulator

#%%
if __name__ == "__main__":
    from os.path import dirname, join, realpath, basename
    folder = join(dirname(dirname(realpath(__file__))), "data")
    instructions = parser(f"{folder}/day08.txt")

    _, accumulator = run_instructions(instructions)
    print("Part 1 —", accumulator)
    print("Part 2 —", fix_instructions(instructions))

