# Dec 19, 2016

"""
--- Day 19: An Elephant Named Joseph ---

The Elves contact you over a highly secure emergency channel. Back at the North Pole, the Elves are busy
misunderstanding White Elephant parties.

Each Elf brings a present. They all sit in a circle, numbered starting with position 1. Then, starting with the
first Elf, they take turns stealing all the presents from the Elf to their left. An Elf with no presents is removed
from the circle and does not take turns.

For example, with five Elves (numbered 1 to 5):

  1
5   2
 4 3
Elf 1 takes Elf 2's present.
Elf 2 has no presents and is skipped.
Elf 3 takes Elf 4's present.
Elf 4 has no presents and is also skipped.
Elf 5 takes Elf 1's two presents.
Neither Elf 1 nor Elf 2 have any presents, so both are skipped.
Elf 3 takes Elf 5's three presents.
So, with five Elves, the Elf that sits starting in position 3 gets all the presents.

With the number of Elves given in your puzzle input, which Elf gets all the presents?

Your puzzle input is 3004953.
"""

my_input = 3004953

gifts = {s+1: 1 for s in range(my_input)}

elf = 1
while len(gifts) > 1:
    if elf not in gifts.keys():
        elf = (elf % my_input) + 1
        continue

    # print(elf, gifts)

    next_elf = (elf % my_input) + 1
    while next_elf not in gifts.keys():
        next_elf = (next_elf % my_input) + 1

    gifts[elf] += gifts.pop(next_elf)
    elf = next_elf

print('Answer: {}'.format(gifts))

"""
--- Part Two ---

Realizing the folly of their present-exchange rules, the Elves agree to instead steal presents from the Elf directly
across the circle. If two Elves are across the circle, the one on the left (from the perspective of the stealer) is
stolen from. The other rules remain unchanged: Elves with no presents are removed from the circle entirely, and the
other elves move in slightly to keep the circle evenly spaced.

For example, with five Elves (again numbered 1 to 5):

The Elves sit in a circle; Elf 1 goes first:
  1
5   2
 4 3
Elves 3 and 4 are across the circle; Elf 3's present is stolen, being the one to the left. Elf 3 leaves the circle,
and the rest of the Elves move in:
  1           1
5   2  -->  5   2
 4 -          4
Elf 2 steals from the Elf directly across the circle, Elf 5:
  1         1
-   2  -->     2
  4         4
Next is Elf 4 who, choosing between Elves 1 and 2, steals from Elf 1:
 -          2
    2  -->
 4          4
Finally, Elf 2 steals from Elf 4:
 2
    -->  2
 -
So, with five Elves, the Elf that sits starting in position 2 gets all the presents.

With the number of Elves given in your puzzle input, which Elf now gets all the presents?
"""

from math import floor
import numpy as np

my_input = 5
# my_input = 3004953
# my_input = 100

def elf_circle2(my_input):
    elf_list = [s+1 for s in range(my_input)]

    ind = 0
    # print('{} ({}): {}'.format(ind, elf_list[ind], elf_list))
    while len(elf_list) > 1:
        elf_curr = elf_list[ind]
        steal_ind = floor(len(elf_list) / 2) + ind
        steal_ind %= len(elf_list)

        elf_list.pop(steal_ind)
        ind = np.where(np.array(elf_list) == elf_curr)[0][0]

        ind += 1
        ind %= len(elf_list)

        # print('{} ({}): {}'.format(ind, elf_list[ind], elf_list))

    return elf_list

# Finally got elf_circle2 to work

# I can see a pattern!
# Trying to replicate it

# Pattern is hard to write, but this was on reddit.
# https://www.reddit.com/r/adventofcode/comments/5j4lp1/2016_day_19_solutions/dbdobax/
from math import log
def part2(n):
    p = 3**int(log(n-1, 3))
    return n - p + max(n-2*p, 0)

for i in range(5, 50):
    winner = elf_circle2(i)[0]
    print('{}: {} {}'.format(i, winner, part2(i)))

print('Answer: {}'.format(part2(3004953)))
