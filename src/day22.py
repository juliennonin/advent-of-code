# %%
def parser(filename):
    with open(filename) as f:
        deck1, deck2 = f.read().split("\n\n")
        deck1 = [int(i) for i in deck1.split('\n')[1:]]
        deck2 = [int(i) for i in deck2.split('\n')[1:]]
    return deck1, deck2

# %%
def deck_score(deck):
    n = len(deck)
    return sum((n - i) * card for i, card in enumerate(deck))

# %%
def play_combat(deck1, deck2, recursive=True):
    p, q = list(deck1), list(deck2)
    mem = set()

    while len(p) != 0 and len(q) != 0:        
        idx = f"{deck_score(p)}-{deck_score(q)}"
        if idx in mem:
            # This round has already been played
            return 0, []
        mem.add(idx)
      
        a, b = p.pop(0), q.pop(0)
        if recursive and len(p) >= a and len(q) >= b:
            # Play recursive game
            winner, _ = play_combat(p[:a], q[:b])
        
        else:
            # Not enough card in their deck (or version 1 w/o recursion)
            winner = 0 if a > b else 1
        
        if winner == 0:
            p.extend([a, b])
        else:
            q.extend([b, a])

    return (0, p) if p else (1, q)

#%%
if __name__ == "__main__":
    from os.path import dirname, join, realpath
    folder = join(dirname(dirname(realpath(__file__))), "data")    
    p, q = parser(f"{folder}/day22.txt")

    print("Part 1 —", deck_score(play_combat(p, q, recursive=False)[1]))
    print("Part 1 —", deck_score(play_combat(p, q, recursive=True)[1]))

