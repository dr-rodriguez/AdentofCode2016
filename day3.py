# Dec 3, 2016

"""
--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways and office furniture that makes up
this part of Easter Bunny HQ. This must be a graphic design department; the walls are covered in
specifications for triangles.

Or are they?

The design document gives the side lengths of each triangle it describes, but... 5 10 25?
Some of these aren't triangles. You can't help but mark the impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining side.
For example, the "triangle" given above is impossible, because 5 + 10 is not larger than 25.

In your puzzle input, how many of the listed triangles are possible?
"""

import numpy as np

count = 0
with open('data/day3_input.txt') as f:
    for line in f:
        values = [int(x) for x in line.split()]
        values = np.sort(values)
        if values[0] + values[1] > values[2]:
            print("Good: {}".format(' '.join([str(x) for x in values])))
            count += 1

print('Answer: {}'.format(count))

"""
--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to you that triangles are
specified in groups of three vertically. Each set of three numbers in a column specifies a triangle.
Rows are unrelated.

For example, given the following specification, numbers with the same hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?
"""

# Need to read the entire set, transpose it so columns are rows, and then reshape for only 3 new columns

data = np.loadtxt('data/day3_input.txt')
len_data = len(data)
data = data.T.reshape((len_data, 3))

count = 0
for values in data:
    values = np.sort(values)
    if values[0] + values[1] > values[2]:
        print("Good: {}".format(' '.join([str(x) for x in values])))
        count += 1

print('Answer: {}'.format(count))
