#%%
import re
from functools import reduce

#%%
def _build_rule(ranges):
    R = []
    for r in ranges:
        start, stop = r.split('-')
        start, stop = int(start), int(stop) + 1
        R.append(range(start, stop))
    return lambda x: any([x in r for r in R])


def parser(filename):
    """
    Returns:
        fields_rules [dict]: field_name -> function that checks if a field respect the rule
        my_ticket [list of int]: field value of my ticket
        tickets [list of list of int]: list of tickets
    """
    with open(filename) as f:
        rules_raw, my_ticket_raw, tickets_raw= f.read().split("\n\n")
    
    fields_rules = {}
    for rule in rules_raw.split("\n"):
        field, *ranges = re.search('(.*): (.*) or (.*)', rule).groups()
        fields_rules[field] = _build_rule(ranges)

    my_ticket = list(map(int, my_ticket_raw.split('\n')[1].split(',')))
    tickets = [list(map(int, ticket.split(','))) for ticket in tickets_raw.split('\n')[1:-1]]

    return fields_rules, my_ticket, tickets

# %%
def remove_invalid_tickets(rules, tickets):
    invalid_fields = []
    valid_tickets = []
    for ticket in tickets:
        ticket_is_valid = True
        for field in ticket:
            field_is_valid = any(rule(field) for rule in rules.values())
            if not field_is_valid:
                invalid_fields.append(field)
                ticket_is_valid = False
        if ticket_is_valid:
            valid_tickets.append(ticket)
    return invalid_fields, valid_tickets

# %%
def find_impossible_field_index(rules, tickets):
    fields_impossible_index = {k:set() for k in rules}  # field_name -> set of impossible indices
    for ticket in tickets:
        for i, field in enumerate(ticket):
            for field_name, rule in rules.items():
                if not rule(field):
                    fields_impossible_index[field_name].add(i)
    return fields_impossible_index


def find_field_position(fields_not_indices):
    fields_to_solve = sorted(fields_not_indices.keys(), key=lambda k: len(fields_not_indices[k]), reverse=True)
    remaining_indices = set(range(len(fields_not_indices)))
    fields_index_map = {}
    for field in fields_to_solve:
        inter = remaining_indices - fields_not_indices[field]
        assert len(inter) == 1, "Not solvable"
        fields_index_map[field] = list(inter)[0]
        remaining_indices -= inter
    return fields_index_map


# %%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")
    prod = lambda L: reduce(lambda x, y: x * y, L)
    
    rules, my_ticket, all_tickets = parser(f"{folder}/day16.txt")
    invalid_fields, tickets = remove_invalid_tickets(rules, all_tickets)
    fields_impossible_index = find_impossible_field_index(rules, tickets)
    fields_index_map = find_field_position(fields_impossible_index)

    departure_field_names = [field for field in fields_index_map if field.startswith("departure")]
    print("Part 1 —", sum(invalid_fields))
    print("Part 2 —", prod(my_ticket[fields_index_map[field]] for field in departure_field_names))
        
# %%
