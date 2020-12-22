# %%
def parser(filename):
    passports = []
    with open(filename) as f:
        data = f.read().replace('\n', ' ').split("  ")  # one line -> one passport
    
    for line in data:
        passport = {}
        for field_value in line.split(' '):
            field, value = field_value.split(':')
            passport[field] = value
        passports.append(passport)
    
    return passports

# %%
constraints = {
    'byr': lambda byr: 1920 <= int(byr) <= 2002,
    'iyr': lambda iyr: 2010 <= int(iyr) <= 2020,
    'eyr': lambda eyr: 2020 <= int(eyr) <= 2030,
    'hgt': lambda hgt: {"cm": hgt[:-2] and 150 <= int(hgt[:-2]) <= 193,
                        "in": hgt[:-2] and 59 <= int(hgt[:-2]) <= 76}.get(hgt[-2:], False),
    'hcl': lambda hcl: hcl[0] == "#" and hcl[1:].isalnum(),
    'ecl': lambda ecl: ecl in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    'pid': lambda pid: len(pid) == 9 and pid.isdigit(),
    'cid': lambda cid: True
}

no_constraints = {field: lambda x: True for field in constraints}

def passport_checker(passport, constraints, opt_fields={'cid'}):
    has_all_required_fields = (set(constraints.keys()) - opt_fields <= set(passport.keys()))
    has_all_correct_fields = all(constraints[field](value) for field, value in passport.items())
    return has_all_required_fields and has_all_correct_fields

# %%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")
    passports = parser(f"{folder}/day04.txt")

    print("Part 1 —",
        sum(passport_checker(p, no_constraints) for p in passports))
    print("Part 2 —",
        sum(passport_checker(p, constraints) for p in passports))

