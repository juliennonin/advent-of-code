# %%
import re
from utils import memoize

# %%
def parser(filename):
    bags_out = {} # bag B can be contained in the bags_out[B]
    bags_in = {}  # bags_in[B] is a list of tuples (N, bag_type), such that bag B contains N bags of type bag_type
    
    with open(filename) as f:
        data = f.read().splitlines()
    
    for i, line in enumerate(data):
        container = re.search("\w* \w*", line).group()
        bags_contained = re.findall("(\d) ([a-z]* [a-z]*)", line)  # list of (number, color)
        
        bags_in[container] = []
        bags_out.setdefault(container, [])
        for number, bag in bags_contained:
            bags_in[container].append((int(number), bag))
            bags_out.setdefault(bag, []).append(container)
    
    return bags_out, bags_in


# %%
def number_of_bags_that_contain_b(b, bags_out):
    container = []
    
    def rec(b):
        for bag in bags_out[b]:
            if not bag in container:
                rec(bag)
                container.append(bag)
    rec(b)
    return len(container)


# %%
@memoize
def number_of_bags_contained_in_b(b, bags_in):
    return sum(n * number_of_bags_contained_in_b(bag, bags_in) + n for n, bag in bags_in[b])


#%%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")    
    bags_out, bags_in = parser(f"{folder}/day07.txt")

    print("Part 1 —", number_of_bags_that_contain_b("shiny gold", bags_out))
    print("Part 2 —", number_of_bags_contained_in_b("shiny gold", bags_in=bags_in))

