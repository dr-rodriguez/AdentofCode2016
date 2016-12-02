# Dec 2, 2016

"""
--- Day 2: Bathroom Security ---

You arrive at Easter Bunny Headquarters under cover of darkness. However, you left in such a rush that you forgot to use the bathroom! Fancy office buildings like this one usually have keypad locks on their bathrooms, so you search the front desk for the code.

"In order to improve security," the document you find says, "bathroom codes will no longer be written down. Instead, please memorize and follow the procedure below to access the bathrooms."

The document goes on to explain that each button to be pressed can be found by starting on the previous button and moving to adjacent buttons on the keypad: U moves up, D moves down, L moves left, and R moves right. Each line of instructions corresponds to one button, starting at the previous button (or, for the first line, the "5" button); press whatever button you're on at the end of each line. If a move doesn't lead to a button, ignore it.

You can't hold it much longer, so you decide to figure out the code as you walk to the bathroom. You picture a keypad like this:

1 2 3
4 5 6
7 8 9
Suppose your instructions are:

ULL
RRDDD
LURDL
UUUUD
You start at "5" and move up (to "2"), left (to "1"), and left (you can't, and stay on "1"), so the first button is 1.
Starting from the previous button ("1"), you move right twice (to "3") and then down three times (stopping at "9" after two moves and ignoring the third), ending up with 9.
Continuing from "9", you move left, up, right, down, and left, ending with 8.
Finally, you move up four times (stopping at "2"), then down once, ending with 5.
So, in this example, the bathroom code is 1985.

Your puzzle input is the instructions from the document you found at the front desk. What is the bathroom code?
"""


def proc_command(comm, i_r, i_c):
    # Get the value for the line
    keypad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    if comm == 'D':
        i_r = proc_move(i_r, 1)
    elif comm == 'U':
        i_r = proc_move(i_r, -1)
    elif comm == 'L':
        i_c = proc_move(i_c, -1)
    elif comm == 'R':
        i_c = proc_move(i_c, 1)

    return keypad[i_r][i_c], i_r, i_c


def proc_move(i, change):
    # Move only if not at the edges
    if i == 0 and change == -1:
        return i
    elif i == 2 and change == 1:
        return i
    else:
        return i + change

# Start at 5
i_r = 1
i_c = 1
val = 5
code = list()

with open('data/day2_input.txt') as f:
    for line in f:
        print(line.strip())
        for comm in line.strip():
            val, i_r, i_c = proc_command(comm, i_r, i_c)
        print(val)
        code.append(val)

print('Answer: {}'.format(''.join([str(s) for s in code])))

"""
--- Part Two ---

You finally arrive at the bathroom (it's a several minute walk from the lobby so visitors can behold the many fancy
conference rooms and water coolers on this floor) and go to punch in the code. Much to your bladder's dismay, the
keypad is not at all like you imagined it. Instead, you are confronted with the result of hundreds of man-hours of
bathroom-keypad-design meetings:

    1
  2 3 4
5 6 7 8 9
  A B C
    D
You still start at "5" and stop when you're at an edge, but given the same instructions as above,
the outcome is very different:

You start at "5" and don't move at all (up and left are both edges), ending at 5.
Continuing from "5", you move right twice and down three times (through "6", "7", "B", "D", "D"), ending at D.
Then, from "D", you move five more times (through "D", "B", "C", "C", "B"), ending at B.
Finally, after five more moves, you end at 3.
So, given the actual keypad layout, the code would be 5DB3.

Using the same instructions in your puzzle input, what is the correct bathroom code?
"""


def real_keypad(comm, i_r, i_c):
    # Get the value for the line, with built in checks
    keypad = [[0,0,1,0,0], [0,2,3,4,0], [5,6,7,8,9], [0,'A','B','C',0], [0,0,'D',0,0]]

    if comm == 'D':
        i_r, i_c = proc_move2(i_r, i_c, 1, 0, keypad)
    elif comm == 'U':
        i_r, i_c = proc_move2(i_r, i_c, -1, 0, keypad)
    elif comm == 'L':
        i_r, i_c = proc_move2(i_r, i_c, 0, -1, keypad)
    elif comm == 'R':
        i_r, i_c = proc_move2(i_r, i_c, 0, 1, keypad)

    return keypad[i_r][i_c], i_r, i_c


def proc_move2(i_r, i_c, change_r, change_c, keypad):
    # Move only if not at the edges, use the odd keypad shape
    if i_c == 0 and change_c == -1:
        return i_r, i_c
    elif i_c == 4 and change_c == 1:
        return i_r, i_c
    elif i_r == 0 and change_r == -1:
        return i_r, i_c
    elif i_r == 4 and change_r == 1:
        return i_r, i_c
    else:
        new_r = i_r + change_r
        new_c = i_c + change_c
        val = keypad[new_r][new_c]
        if val == 0:
            return i_r, i_c
        else:
            return new_r, new_c

# Start at 5
i_r = 2
i_c = 0
val = 5
code = list()

with open('data/day2_input.txt') as f:
    for line in f:
        print(line.strip())
        for comm in line.strip():
            val, i_r, i_c = real_keypad(comm, i_r, i_c)
        print(val)
        code.append(val)

print('Answer: {}'.format(''.join([str(s) for s in code])))
