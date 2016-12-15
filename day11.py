# Dec 11, 2016

"""
--- Day 11: Radioisotope Thermoelectric Generators ---

You come upon a column of four floors that have been entirely sealed off from the rest of the building except for a
small dedicated lobby. There are some radiation warnings and a big sign which reads "Radioisotope Testing Facility".

According to the project status board, this facility is currently being used to experiment with Radioisotope
Thermoelectric Generators (RTGs, or simply "generators") that are designed to be paired with specially-constructed
microchips. Basically, an RTG is a highly radioactive rock that generates electricity through heat.

The experimental RTGs have poor radiation containment, so they're dangerously radioactive. The chips are prototypes
and don't have normal radiation shielding, but they do have the ability to generate an electromagnetic radiation
shield when powered. Unfortunately, they can only be powered by their corresponding RTG. An RTG powering a microchip
is still dangerous to other microchips.

In other words, if a chip is ever left in the same area as another RTG, and it's not connected to its own RTG, the
chip will be fried. Therefore, it is assumed that you will follow procedure and keep chips connected to their
corresponding RTG when they're in the same room, and away from other RTGs otherwise.

These microchips sound very interesting and useful to your current activities, and you'd like to try to retrieve them.
The fourth floor of the facility has an assembling machine which can make a self-contained, shielded computer for you
to take with you - that is, if you can bring it all of the RTGs and microchips.

Within the radiation-shielded part of the facility (in which it's safe to have these pre-assembly RTGs), there is an
elevator that can move between the four floors. Its capacity rating means it can carry at most yourself and two RTGs
or microchips in any combination. (They're rigged to some heavy diagnostic equipment - the assembling machine will
detach it for you.) As a security measure, the elevator will only function if it contains at least one RTG or
microchip. The elevator always stops on each floor to recharge, and this takes long enough that the items within it
and the items on that floor can irradiate each other. (You can prevent this if a Microchip and its Generator end up
on the same floor in this way, as they can be connected while the elevator is recharging.)

You make some notes of the locations of each component of interest (your puzzle input). Before you don a hazmat suit
and start moving things around, you'd like to have an idea of what you need to do.

When you enter the containment area, you and the elevator will start on the first floor.

For example, suppose the isolated area has the following arrangement:

The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
As a diagram (F# for a Floor number, E for Elevator, H for Hydrogen, L for Lithium, M for Microchip, and G for
Generator), the initial state looks like this:

F4 .  .  .  .  .
F3 .  .  .  LG .
F2 .  HG .  .  .
F1 E  .  HM .  LM
Then, to get everything up to the assembling machine on the fourth floor, the following steps could be taken:

Bring the Hydrogen-compatible Microchip to the second floor, which is safe because it can get power from the
Hydrogen Generator:

F4 .  .  .  .  .
F3 .  .  .  LG .
F2 E  HG HM .  .
F1 .  .  .  .  LM
Bring both Hydrogen-related items to the third floor, which is safe because the Hydrogen-compatible microchip is
getting power from its generator:

F4 .  .  .  .  .
F3 E  HG HM LG .
F2 .  .  .  .  .
F1 .  .  .  .  LM
Leave the Hydrogen Generator on floor three, but bring the Hydrogen-compatible Microchip back down with you so you
can still use the elevator:

F4 .  .  .  .  .
F3 .  HG .  LG .
F2 E  .  HM .  .
F1 .  .  .  .  LM
At the first floor, grab the Lithium-compatible Microchip, which is safe because Microchips don't affect each other:

F4 .  .  .  .  .
F3 .  HG .  LG .
F2 .  .  .  .  .
F1 E  .  HM .  LM
Bring both Microchips up one floor, where there is nothing to fry them:

F4 .  .  .  .  .
F3 .  HG .  LG .
F2 E  .  HM .  LM
F1 .  .  .  .  .
Bring both Microchips up again to floor three, where they can be temporarily connected to their corresponding
generators while the elevator recharges, preventing either of them from being fried:

F4 .  .  .  .  .
F3 E  HG HM LG LM
F2 .  .  .  .  .
F1 .  .  .  .  .
Bring both Microchips to the fourth floor:

F4 E  .  HM .  LM
F3 .  HG .  LG .
F2 .  .  .  .  .
F1 .  .  .  .  .
Leave the Lithium-compatible microchip on the fourth floor, but bring the Hydrogen-compatible one so you can still
use the elevator; this is safe because although the Lithium Generator is on the destination floor, you can connect
Hydrogen-compatible microchip to the Hydrogen Generator there:

F4 .  .  .  .  LM
F3 E  HG HM LG .
F2 .  .  .  .  .
F1 .  .  .  .  .
Bring both Generators up to the fourth floor, which is safe because you can connect the Lithium-compatible Microchip
to the Lithium Generator upon arrival:

F4 E  HG .  LG LM
F3 .  .  HM .  .
F2 .  .  .  .  .
F1 .  .  .  .  .
Bring the Lithium Microchip with you to the third floor so you can use the elevator:

F4 .  HG .  LG .
F3 E  .  HM .  LM
F2 .  .  .  .  .
F1 .  .  .  .  .
Bring both Microchips to the fourth floor:

F4 E  HG HM LG LM
F3 .  .  .  .  .
F2 .  .  .  .  .
F1 .  .  .  .  .
In this arrangement, it takes 11 steps to collect all of the objects at the fourth floor for assembly. (Each
elevator stop counts as one step, even if nothing is added to or removed from it.)

In your situation, what is the minimum number of steps required to bring all of the objects to the fourth floor?
"""

# This is an extremely hard puzzle to code
# After reading code on reddit for several days I now understand what to do better
# The best approach is a breadth-first search or A* search, which I now know thanks to puzzle 13
# We will sample all possibilities, ruling out the bad ones until we find the ideal solution
# Good reddit references:
# https://www.reddit.com/r/adventofcode/comments/5hoia9/2016_day_11_solutions/db1zbu0/
# https://www.reddit.com/r/adventofcode/comments/5hoia9/2016_day_11_solutions/db1v1ws/
# In the end, I copied over the first reference's code, but heavily commented it so I could understand what happens

from itertools import combinations
import heapq
# This module provides an implementation of the heap queue algorithm, also known as the priority queue algorithm.
# Heaps are binary trees for which every parent node has a value less than or equal to any of its children.

# Test input
# The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
# The second floor contains a hydrogen generator.
# The third floor contains a lithium generator.
# The fourth floor contains nothing relevant.
# hydrogen, lithium = 1, 2
# initial = (0, (                                      # initial floor
#             tuple(sorted((-hydrogen, -lithium))),    # floor 0, chips are negative
#             (hydrogen),                              # floor 1, generators are positive
#             (lithium),                               # floor 2
#             ()))                                     # floor 3

# My input
"""
The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, and a plutonium-compatible microchip.
The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
The third floor contains a thulium-compatible microchip.
The fourth floor contains nothing relevant.
"""
strontium, plutonium, thulium, ruthenium, curium = 1, 2, 3, 4, 5
initial = (0, (
    tuple(sorted((strontium, -strontium, plutonium, -plutonium))),
    tuple(sorted((thulium, ruthenium, -ruthenium, curium, -curium))),
    (-thulium),
    ()
))


def correct(floor):
    # Function to test the floor is valid
    if not floor or floor[-1] < 0:  # no generators (due to sorting, generators always last)
        return True
    # The following checks that all chips in a floor are accompanied by the inverse (ie, a corresponding generator)
    return all(-chip in floor for chip in floor if chip < 0)

frontier = []
heapq.heappush(frontier, (0, initial))
# This is a dictionary whose keys are the floor configurations and values are the number of moves it took to get there
cost_so_far = {initial: 0}

while frontier:
    _, current = heapq.heappop(frontier)
    floor, floors = current
    if floor == 3 and all(len(f) == 0 for f in floors[:-1]):  # Goal: at top floor with nothing on the others
        break

    # Get valid directions (down, up) constraining them so they don't go below floor 0 or above floor 3
    directions = [dir for dir in (-1, 1) if 0 <= floor + dir < 4]
    # Generate all possible moves from the current floor by moving 1 item or 2 items
    moves = list(combinations(floors[floor], 2)) + list(combinations(floors[floor], 1))
    for move in moves:
        for direction in directions:
            # Generate new floor configuration
            new_floors = list(floors)  # copy of current floors configuration
            # Floor we were on gets all the items it had before, minus the ones we moved:
            new_floors[floor] = tuple(x for x in floors[floor] if x not in move)
            # Floor we moved to gets the items it had before, plus those we moved:
            try:
                new_floors[floor+direction] = tuple(sorted(floors[floor+direction] + move))
            except TypeError:  # for cases where there is only 1 item in the new floor
                new_floors[floor + direction] = tuple(sorted([floors[floor + direction]] + list(move)))

            # Test that both the old floor and new floor are valid, otherwise skip the rest
            if not correct(new_floors[floor]) or not correct(new_floors[floor+direction]):
                continue

            # New tuple like initial: this is the description of what floor we are in & the floor configuration
            next = (floor+direction, tuple(new_floors))
            new_cost = cost_so_far[current] + 1  # increment the number of moves taken

            # If we haven't encountered this floor configuration before,
            # or if we have and we have done so in less moves:
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                # heapq requires a priority, here the original author set it to be the cost minus 10 times the number
                # of items in the top floor. This prioritizes filling up the top floor
                # For my input, had to tweak these by removing the * 10 part
                priority = new_cost - len(new_floors[3])*1
                heapq.heappush(frontier, (priority, next))

            # NOTE: This is missing some optimization and so extra moves are considered, see the second reddit link

print(cost_so_far[current], current)
# 39 is too high for part 1, had to tweak the prioritization

"""
--- Part Two ---

You step into the cleanroom separating the lobby from the isolated area and put on the hazmat suit.

Upon entering the isolated containment area, however, you notice some extra parts on the first floor that weren't
listed on the record outside:

An elerium generator.
An elerium-compatible microchip.
A dilithium generator.
A dilithium-compatible microchip.
These work just like the other generators and microchips. You'll have to get them up to assembly as well.

What is the minimum number of steps required to bring all of the objects, including these four new ones,
to the fourth floor?
"""

# My new input:
strontium, plutonium, thulium, ruthenium, curium, elerium, dilithium = 1, 2, 3, 4, 5, 6, 7
initial = (0, (
    tuple(sorted((strontium, -strontium, plutonium, -plutonium, elerium, -elerium, dilithium, -dilithium))),
    tuple(sorted((thulium, ruthenium, -ruthenium, curium, -curium))),
    (-thulium),
    ()
))

# Re-run the code above. This part takes much longer due to lack of optimization.
