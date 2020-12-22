# %%
def create_mask_v1(mask):
    mask1 = int(mask.replace("X", '0'), 2)
    mask2 = int(mask.replace("X", '1'), 2)
    return lambda x : (x | mask1) & mask2

# %%
def create_mask_v2(mask):
    def apply_mask(x):
        x_bin = list(bin(x)[2:].zfill(len(mask)))
        for i, oct in enumerate(mask):
            if oct != "0":
                x_bin[i] = oct
        return ''.join(x_bin)
    return apply_mask

def generate_addresses(ad):
    if "X" in ad:
        yield from generate_addresses(ad.replace("X", "0", 1))
        yield from generate_addresses(ad.replace("X", "1", 1))
    else:
        yield int(ad, 2)
    
#%%
def run_script(data, part):
    mem = {}
    for instr in data:
        if instr[:4] == "mask":
            apply_mask = create_mask_v1(instr[7:]) if part == 1 else create_mask_v2(instr[7:])
        else:
            loc, value = map(int, instr[4:].split('] = '))
            if part == 1:
                mem[loc] = apply_mask(value)
            elif part == 2:
                for ad in generate_addresses(apply_mask(loc)):
                    mem[ad] = value
    return mem


#%%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")
    with open(f"{folder}/day14.txt") as f:
        data = f.read().splitlines()    

    print("Part 1 —", sum(run_script(data, part=1).values()))
    print("Part 2 —", sum(run_script(data, part=2).values()))
