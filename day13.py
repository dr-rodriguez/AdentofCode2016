# Dec 13, 2016

"""
--- Day 13: A Maze of Twisty Little Cubicles ---

You arrive at the first floor of this new building to discover a much less welcoming environment than the shiny
atrium of the last one. Instead, you are in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative integers (x,y). Each such coordinate is either a
wall or an open space. You can't move diagonally. The cube maze starts at 0,0 and seems to extend infinitely toward
positive x and y; negative values are invalid, as they represent a location outside the building. You are in a small
waiting area at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains, the layout is actually quite logical. You can
determine whether a given x,y coordinate will be a wall or an open space using a simple system:

Find x*x + 3*x + 2*x*y + y + y*y.
Add the office designer's favorite number (your puzzle input).
Find the binary representation of that sum; count the number of bits that are 1.
If the number of bits that are 1 is even, it's an open space.
If the number of bits that are 1 is odd, it's a wall.
For example, if the office designer's favorite number were 10, drawing walls as # and open spaces as ., the corner of
the building containing 0,0 would look like this:

  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###
Now, suppose you wanted to reach 7,4. The shortest route you could take is marked as O:

  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###
Thus, reaching 7,4 would take a minimum of 11 steps (starting from your current location, 1,1).

What is the fewest number of steps required for you to reach 31,39?
"""

# My brute-force approach works for the test input (probably dumb luck), but not for the actual input.
# Too many paths to consider and it keeps getting stuck on bad paths.

# Looking through reddit this is another example of depth-first search or breadth-first search,
# similar to Day 11, which I haven't yet solved.
# I kept some of my code attempts, but skip down to ====== for the solution.

my_input = 1362

def gen_space(x, y):
    global my_input

    v = x*x + 3*x + 2*x*y + y + y*y + my_input
    v = bin(v).count('1')  # get binary representation and count 1s
    return v % 2 == 0 and x >= 0 and y >= 0
    # if v % 2 == 0:
    #     return True  # open space
    # else:
    #     return False  # wall

def move_path(x, y, curr_dir):
    # Prioritize down, right, up, left unless curr_dir is provided
    global bad_loc

    if gen_space(x, y-1) and 0 not in avoid_dir:  # Try up
        y -= 1
        curr_dir = 0
    elif gen_space(x - 1, y) and 3 not in avoid_dir:  # Try left
        x -= 1
        curr_dir = 3
    elif gen_space(x, y+1) and 2 not in avoid_dir:  # Try down
        y += 1
        curr_dir = 2
    elif gen_space(x+1, y) and 1 not in avoid_dir:  # Try right
        x += 1
        curr_dir = 1
    else:  # no valid path found, skip back and reset
        # print('Got caught')
        bad_loc.append((x, y))
        # return -9, -9, curr_dir

    return x, y, curr_dir

def gen_mini_map(x, y):
    my_map = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
    for i in range(5):
        for j in range(5):
            if gen_space(x+i-2, y+j-2):
                my_map[j][i] = '.'
            else:
                my_map[j][i] = '#'
            # print(x+i-2, y+j-2, my_map[j][i])
    for row in my_map:
        print(row)

gen_mini_map(21, 16)

x = 7
y = 4
# x = 31
# y = 39
path = [(x,y)]
orig_dir = 0
curr_dir = 0
avoid_dir = list()
count = 0
bad_loc = list()
repetition_dict = dict()
path_dict = dict()
for i in range(100):
# while (1,1) not in path:
    print(x, y, curr_dir)

    # Check if in a bad location
    # if (x, y) in bad_loc:
    #     print('Known bad location')
    #     x, y = path.pop()
    #     print('New values: {} {}'.format(x, y))

    if x == 1 and y == 1:
        print('Reached start')
        print(len(path))
        break

    if count > 4:
        count = 0
        x, y = path.pop()
        avoid_dir = list()

    x, y, curr_dir = move_path(x, y, curr_dir)

    if (x, y) in path:
        print('Repetition: {} {}'.format(x, y))
        loc = '{} {}'.format(x, y)
        if loc not in repetition_dict.keys():
            repetition_dict[loc] = 1
        else:
            repetition_dict[loc] += 1

        # Avoid running the same direction or landing on the same space
        if repetition_dict[loc] > 3:  # stop repeating and go back one more
            print('Count reached for {}'.format(loc))
            if (x, y) in bad_loc:
                x, y = path.pop()
            else:
                bad_loc.append((x, y))
            x, y = path.pop()
            # print('New values: {} {}'.format(x,y))
        # else:
        x, y = path.pop()
        avoid_dir.append(curr_dir)  # to avoid running the same one
        count += 1
        print('New values: {} {}'.format(x, y))
    else:
        print('Adding {} {}'.format(x, y))
        path.append((x, y))
        avoid_dir = list()


# ==============================
# Edited but mostly from reddit:
# https://www.reddit.com/r/adventofcode/comments/5i1q0h/2016_day_13_solutions/db4qgz8/
# Original does not work in Python 3 due to dictionary keys being tuples, but now it works

frontier = [(1, 1, 0)]
explored = {}
my_input = 1362

def get_wall(tup):
    # Check if there's a space (True) or a wall (False)
    global my_input
    num = tup[0] * tup[0] + 3 * tup[0] + 2 * tup[0] * tup[1] +tup[1] + tup[1] * tup[1] + my_input
    return bin(num)[2:].count("1") % 2 == 0 and tup[0] >= 0 and tup[1] >= 0

def get_next(tup):
    # Returns tuple with x, y, counter for all cases where there is no wall in the immediate four directions
    cand = [(0,1), (0,-1), (1,0), (-1,0)]
    return [(x[0] + tup[0], x[1] + tup[1], tup[2] + 1) for x in cand if get_wall((x[0] + tup[0], x[1] + tup[1]))]

# This is an example of a non-recursive depth-first-search (DFS; as opposed to a breadth-first-search)
# The loop proceeds to empty out frontier by creating explored, which contains each location and how long it took to
# reach it. Explored is filled out by going deep in each node and saving the best value.
while len(frontier) > 0:
    # print(frontier)
    new = frontier.pop()
    loc = '{} {}'.format(new[0], new[1])
    explored[loc] = new[2]
    frontier += [x for x in get_next(new) if not '{} {}'.format(x[0], x[1]) in explored
                 or explored['{} {}'.format(x[0], x[1])] > x[2]]
    # Note that frontier grows as new locations get discovered (ie, not in explored) or the previous explored location
    # has a value larger than the current value (x[2])

print(explored['31 39'])

"""
--- Part Two ---

How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?
"""

print(len([explored[x] for x in explored.keys() if explored[x] <= 50]))
