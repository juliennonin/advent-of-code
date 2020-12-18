#%%
def find_pair_of_brackets(s):
    """ Find positions of one pair of brackets"""
    count = 1
    beg = s.find("(")
    i = beg
    while count != 0:
        i += 1
        if s[i] == "(":
            count += 1
        elif s[i] == ")":
            count -= 1
    return beg, i

def evaluate(s, part):
    assert part == 1 or part == 2
    
    if '(' not in s and ')' not in s:
        if part == 1:
            return eval(t = "("*s.count("*") + s.replace(" *", ") *"))
        elif part == 2:
            return eval("(" + s.replace(" * ", ") * (") + ")")
    
    else: # solve recursively operations inside parentheses
        a, b = find_pair_of_brackets(s)
        sub = s[a:b+1]
        val = evaluate(sub[1:-1], part)  # sub[1:-1] to strip parentheses around sub
        return evaluate(s.replace(sub, str(val)), part)

#%%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")
    with open(f"{folder}/day18.txt") as f:
        data = f.read().splitlines()

    print("Part 1 —", sum(evaluate(line, part=1) for line in data))
    print("Part 2 —", sum(evaluate(line, part=2) for line in data))
