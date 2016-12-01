# Dec 1, 2016

"""
You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", unfortunately, is as close as you can get
- the instructions on the Easter Bunny Recruiting Document the Elves intercepted start here,
and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates (where you just landed) and face North.
Then, follow the provided sequence: either turn left (L) or right (R) 90 degrees, then walk forward the given number of
blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you take a moment and work out the
destination. Given that you can only walk on the street grid of the city, how far is the shortest path to the
destination?

For example:

Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
R5, L5, R5, R3 leaves you 12 blocks away.
How many blocks away is Easter Bunny HQ?
"""

# Part 1
my_input = 'R2, L5, L4, L5, R4, R1, L4, R5, R3, R1, L1, L1, R4, L4, L1, R4, L4, R4, L3, R5, R4, R1, R3, L1, L1, R1, L2, R5, L4, L3, R1, L2, L2, R192, L3, R5, R48, R5, L2, R76, R4, R2, R1, L1, L5, L1, R185, L5, L1, R5, L4, R1, R3, L4, L3, R1, L5, R4, L4, R4, R5, L3, L1, L2, L4, L3, L4, R2, R2, L3, L5, R2, R5, L1, R1, L3, L5, L3, R4, L4, R3, L1, R5, L3, R2, R4, R2, L1, R3, L1, L3, L5, R4, R5, R2, R2, L5, L3, L1, L1, L5, L2, L3, R3, R3, L3, L4, L5, R2, L1, R1, R3, R4, L2, R1, L1, R3, R3, L4, L2, R5, R5, L1, R4, L5, L5, R1, L5, R4, R2, L1, L4, R1, L1, L1, L5, R3, R4, L2, R1, R2, R1, R1, R3, L5, R1, R4'

# 0: 'N', 1: 'E', 2: 'S', 3: 'W'
curr_direction = 0
dist_traveled = [0, 0, 0, 0]

path = my_input.split(',')
path = [s.strip() for s in path]
for instruction in path:
    direction = instruction[0]
    length = int(instruction[1:].strip())
    print(direction, length)

    if direction == 'R':
        change = 1
    else:
        change = -1

    curr_direction = (curr_direction + change) % 4
    dist_traveled[curr_direction] += length

print(dist_traveled)
total_dist = abs(dist_traveled[0] - dist_traveled[2]) + abs(dist_traveled[1] - dist_traveled[3])
print('Answer: {}'.format(total_dist))

"""
--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting Document.
Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?
"""

present = [0, 0]
curr_direction = 0
locations = list()
p_string = '{},{}'.format(present[0], present[1])
locations.append(p_string)
found = False

for instruction in path:
    direction = instruction[0]
    length = int(instruction[1:].strip())
    print(direction, length)

    if direction == 'R':
        change = 1
    else:
        change = -1

    curr_direction = (curr_direction + change) % 4
    print(curr_direction)

    if curr_direction == 0:
        ind = 0
        sign = 1
    elif curr_direction == 1:
        ind = 1
        sign = 1
    elif curr_direction == 2:
        ind = 0
        sign = -1
    elif curr_direction == 3:
        ind = 1
        sign = -1

    for i in range(0, length):
        present[ind] += sign
        p_string = '{},{}'.format(present[0], present[1])
        print(p_string)
        if p_string in locations:
            print('Answer found: {} {}'.format(present[0], present[1]))
            print('Solution: {}'.format(abs(present[0]) + abs(present[1])))
            found = True
            break
        locations.append(p_string)

    if found:
        break

# Creating an image for fun
# Adapted from https://www.reddit.com/r/adventofcode/comments/5fvo07/2016_day_1_visualization_of_the_path_taken/danjkmz/
from PIL import Image
import PIL.ImageOps

# Get bounds
maxx, minx, maxy, miny = -10, 10, -10, 10
present = [0, 0]
curr_direction = 0
for instruction in path:
    direction = instruction[0]
    length = int(instruction[1:].strip())

    if direction == 'R':
        change = 1
    else:
        change = -1

    curr_direction = (curr_direction + change) % 4

    if curr_direction == 0:
        ind = 0
        sign = 1
    elif curr_direction == 1:
        ind = 1
        sign = 1
    elif curr_direction == 2:
        ind = 0
        sign = -1
    elif curr_direction == 3:
        ind = 1
        sign = -1

    for i in range(0, length):
        present[ind] += sign
        minx = min(present[1], minx)
        maxx = max(present[1], maxx)
        miny = min(present[0], miny)
        maxy = max(present[0], maxy)

# Start image
x = maxx - minx + 1
y = maxy - miny + 1
img = Image.new('RGB', (x, y))
data = img.load()

# Populate image
present = [0, 0]
curr_direction = 0
for instruction in path:
    direction = instruction[0]
    length = int(instruction[1:].strip())
    print(direction, length)

    if direction == 'R':
        change = 1
    else:
        change = -1

    curr_direction = (curr_direction + change) % 4
    print(curr_direction)

    if curr_direction == 0:
        ind = 0
        sign = 1
    elif curr_direction == 1:
        ind = 1
        sign = 1
    elif curr_direction == 2:
        ind = 0
        sign = -1
    elif curr_direction == 3:
        ind = 1
        sign = -1

    for i in range(0, length):
        present[ind] += sign
        data[present[1] - minx, present[0] - miny] = 255, 255, 255

img = PIL.ImageOps.invert(img)  # invert colors
img.save('images/day1_path.png')
