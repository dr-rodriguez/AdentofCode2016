# Dec 8, 2016

"""
--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an implementation of two-factor authentication
after a long game of requirements telephone.

To get past the door, you first swipe a keycard (no problem; there was one on a nearby desk). Then, it displays a
code on a little screen, and you type that code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've taken everything apart and figured out how
it works. Now you just have to work out what the screen would have displayed.

The magnetic strip on the card you swiped encodes a series of instructions for the screen; these instructions are
your puzzle input. The screen is 50 pixels wide and 6 pixels tall, all of which start off, and is capable of three
somewhat peculiar operations:

rect AxB turns on all of the pixels in a rectangle at the top-left of the screen which is A wide and B tall.
rotate row y=A by B shifts all of the pixels in row A (0 is the top row) right by B pixels. Pixels that would fall
off the right end appear at the left end of the row.
rotate column x=A by B shifts all of the pixels in column A (0 is the left column) down by B pixels. Pixels that
would fall off the bottom appear at the top of the column.
For example, here is a simple sequence on a smaller screen:

rect 3x2 creates a small rectangle in the top-left corner:

###....
###....
.......
rotate column x=1 by 1 rotates the second column down by one pixel:

#.#....
###....
.#.....
rotate row y=0 by 4 rotates the top row right by four pixels:

....#.#
###....
.#.....
rotate column x=1 by 1 again rotates the second column down by one pixel, causing the bottom pixel to wrap
back to the top:

.#..#.#
#.#....
.#.....
As you can see, this display technology is extremely powerful, and will soon dominate the
tiny-code-displaying-screen market. That's what the advertisement on the back of the display tries to
convince you, anyway.

There seems to be an intermediate check of the voltage used by the display: after you swipe your card,
if the screen did work, how many pixels should be lit?
"""

import numpy as np
import re

screen = np.zeros((6, 50))

with open('data/day8_input.txt') as f:
    for line in f:
        command = line.strip()
        print(command)

        if command.startswith('rect '):
            pattern = r'rect (\d+)x(\d+)'
            c, r = re.findall(pattern, command)[0]
            c, r = int(c), int(r)
            for i in range(0, r):
                screen[0:r][i][0:c].fill(1)

        if command.startswith('rotate row'):
            pattern = r'rotate row y=(\d+) by (\d+)'
            r, val = re.findall(pattern, command)[0]
            r, val = int(r), int(val)
            screen[r] = np.roll(screen[r], val)

        if command.startswith('rotate column'):
            pattern = r'rotate column x=(\d+) by (\d+)'
            c, val = re.findall(pattern, command)[0]
            c, val = int(c), int(val)
            screen = screen.T  # transpose to make this easy
            screen[c] = np.roll(screen[c], val)
            screen = screen.T

        print(screen)

print('Answer: {}'.format(screen.sum()))

"""
--- Part Two ---

You notice that the screen is only capable of displaying capital letters; in the font it uses,
each letter is 5 pixels wide and 6 tall.

After you swipe your card, what code is the screen trying to display?
"""

# Convert to string for easier visualization
screen2 = screen.astype(str)
screen2[screen2 == '0.0'] = ' '
screen2[screen2 == '1.0'] = '#'

for j in range(0, screen2.shape[1]):
    if j == 0: continue
    if j % 5 == 4:
        print(j-4, j+1)
        for r in range(0, 6):
            print(screen2[:][r][j-4:j+1])

# Visually inspect to get your specific answer
print('Answer: ZJHRKCPLYJ')
