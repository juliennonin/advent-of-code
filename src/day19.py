#%%
from itertools import product
import time

# %%
def parser(filename):
    with open(filename) as f:
        head, tail = f.read().split("\n\n")
    
    rules = {}
    for rule in head.splitlines():
        idx, rule = rule.split(": ")
        idx = int(idx)
        if '"' in rule:
            rules[idx] = rule.strip('"')
        else:
            rules[idx] = [list(map(int, s.split(' '))) for s in rule.split(' | ')]

    data = tail.splitlines()
    return rules, data

# %%
def memoize(f):
    mem = {}
    def wrap(x, *args, **kwargs):
        if x not in mem:
            mem[x] = f(x, *args, **kwargs)
        return mem[x]
    return wrap

@memoize
def find(i, rules):
    if isinstance(rules[i], str):
        return rules[i]
    
    R = []
    for sub_rule in rules[i]:
        for e in product(*[find(r, rules) for r in sub_rule]):
            R.append(''.join(e))
    return R

# %%
def with_recursive_rules_8_and_11(rules, data):
    """
    pattern: {42}, ..., {42}, {31}, ..., {31}
    with at least one from {42} and one from {31}
    and more {42} than {31}
    """
    assert rules[0] == [[8, 11]]
    assert rules[8] == [[42]]
    assert rules[11] == [[42, 31]]

    pattern_42, pattern_31 = find(42, rules), find(31, rules)
    assert len(pattern_42[0]) == len(pattern_31[0])
    n = len(pattern_42[0])
    pattern_42, pattern_31 = set(pattern_42), set(pattern_31)
    assert pattern_42.isdisjoint(pattern_31)

    valid_msgs = []
    for line in data:
        c_42 = c_31 = 0
        test_42, is_valid = True, True

        for i in range(0, len(line), n):
            sub = line[i:i+n]  # substring of msg of size n

            if test_42:
                if sub in pattern_42:
                    c_42 += 1
                else:
                    test_42 = False
            
            if not test_42:
                if sub in pattern_31:
                    c_31 += 1
                else:
                    is_valid = False
        
        if is_valid and c_42 > c_31 and c_42 > 0 and c_31 > 0:
            valid_msgs.append(line)

    return valid_msgs

#%%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")    
    rules, data = parser(f"{folder}/day19.txt")

    valid_msgs_set = set(find(0, rules))
    print("Part 1 —", sum(msg in valid_msgs_set for msg in data))
    print("Part 2 —", len(with_recursive_rules_8_and_11(rules, data)))