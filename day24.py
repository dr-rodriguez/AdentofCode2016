# Dec 24, 2016

"""
--- Day 24: Air Duct Spelunking ---

You've finally met your match; the doors that provide access to the roof are locked tight, and all of the controls and
related electronics are inaccessible. You simply can't reach them.

The robot that cleans the air ducts, however, can.

It's not a very fast little robot, but you reconfigure it to be able to interface with some of the exposed wires that
have been routed through the HVAC system. If you can direct it to each of those locations, you should be able to
bypass the security controls.

You extract the duct layout for this area from some blueprints you acquired and create a map with the relevant
locations marked (your puzzle input). 0 is your current location, from which the cleaning robot embarks; the other
numbers are (in no particular order) the locations the robot needs to visit at least once each. Walls are marked as
#, and open passages are marked as .. Numbers behave like open passages.

For example, suppose you have a map like the following:

###########
#0.1.....2#
#.#######.#
#4.......3#
###########
To reach all of the points of interest as quickly as possible, you would have the robot take the following path:

0 to 4 (2 steps)
4 to 1 (4 steps; it can't move diagonally)
1 to 2 (6 steps)
2 to 3 (2 steps)
Since the robot isn't very fast, you need to find it the shortest route. This path is the fewest steps (in the above
example, a total of 14) required to start at 0 and then visit every other location at least once.

Given your actual map, and starting from location 0, what is the fewest number of steps required to visit every
non-0 number marked on the map at least once?
"""

from itertools import permutations

with open('data/day24_input.txt', 'r') as f:
    maze = f.read().strip().split('\n')
locations = [0, 1, 2, 3, 4, 5, 6, 7]

# Make location map
map_loc = dict()
for i, row in enumerate(maze):
    for j, char in enumerate(row):
        try:
            char = int(char)
        except:
            continue
        if char in locations:
            map_loc[char] = (i, j)

# 0 is at 17, 149
locations = locations[1:]

# Plan:
# Compute permutations of the locations
# Do DFS or BFS for path to locations
# Select shortest path


def get_wall(tup):
    # Check if there's a space (True) or a wall (False)
    global maze
    val = maze[tup[0]][tup[1]]
    if val == '#':
        return False
    else:
        return True


def get_next(tup):
    # Returns tuple with x, y, counter for all cases where there is no wall in the immediate four directions
    cand = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [(x[0] + tup[0], x[1] + tup[1], tup[2] + 1) for x in cand if get_wall((x[0] + tup[0], x[1] + tup[1]))]


def dfs(start, goal, explored={}):
    global map_loc

    tup = map_loc[start]
    frontier = [(tup[0], tup[1], 0)]

    # This is an example of a non-recursive depth-first-search (DFS; as opposed to a breadth-first-search)
    # The loop proceeds to empty out frontier by creating explored, which contains each location and how long it took to
    # reach it. Explored is filled out by going deep in each node and saving the best value.
    while len(frontier) > 0:
        # print(frontier)
        new = frontier.pop()
        # loc = '{} {}'.format(new[0], new[1])
        loc = '{} {} ({} {})'.format(new[0], new[1], start, goal)
        explored[loc] = new[2]
        # frontier += [x for x in get_next(new) if not '{} {}'.format(x[0], x[1]) in explored
        #              or explored['{} {}'.format(x[0], x[1])] > x[2]]
        frontier += [x for x in get_next(new) if not '{} {} ({} {})'.format(x[0], x[1], start, goal) in explored
                     or explored['{} {} ({} {})'.format(x[0], x[1], start, goal)] > x[2]]
        # Note that frontier grows as new locations get discovered (ie, not in explored) or the previous explored location
        # has a value larger than the current value (x[2])

    tup = map_loc[goal]
    # loc_goal = '{} {}'.format(tup[0], tup[1])
    loc_goal = '{} {} ({} {})'.format(tup[0], tup[1], start, goal)
    # print(explored[loc_goal])
    return explored[loc_goal], explored


solutions = dict()
best = 999999
explored = {}
for new_path in permutations(locations):
    cost = 0
    for c in range(0, 7):
        if c == 0:
            start = 0
        else:
            start = new_path[c-1]
        goal = new_path[c]
        newcost, explored = dfs(start, goal, explored)
        cost += newcost
    print(new_path, cost)
    solutions[new_path] = cost
    best = min(best, cost)

print(best)

"""
--- Part Two ---

Of course, if you leave the cleaning robot somewhere weird, someone is bound to notice.

What is the fewest number of steps required to start at 0, visit every non-0 number marked on the map at least once,
and then return to 0?
"""

solutions = dict()
best = 999999
explored = {}
for new_path in permutations(locations):
    new_path = list(new_path)
    new_path.append(0)
    cost = 0
    for c in range(0, 8):
        if c == 0:
            start = 0
        else:
            start = new_path[c-1]
        goal = new_path[c]
        newcost, explored = dfs(start, goal, explored)
        cost += newcost
    print(new_path, cost)
    solutions[tuple(new_path)] = cost
    best = min(best, cost)

print(best)
