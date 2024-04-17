import itertools
from istr import istr

for s, e, n, d, m, o, r, y in istr(itertools.permutations(range(10), 8)):
    if m and ((s | e | n | d) + (m | o | r | e) == (m | o | n | e | y)):
        print(f" {s|e|n|d}")
        print(f" {m|o|r|e}")
        print("-----")
        print(f"{m|o|n|e|y}")

