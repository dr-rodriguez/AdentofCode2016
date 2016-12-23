# Dec 23, 2016

"""
--- Day 23: Safe Cracking ---

This is one of the top floors of the nicest tower in EBHQ. The Easter Bunny's private office is here, complete with a
safe hidden behind a painting, and who wouldn't hide a star in a safe behind a painting?

The safe has a digital screen and keypad for code entry. A sticky note attached to the safe has a password hint on it:
"eggs". The painting is of a large rabbit coloring some eggs. You see 7.

When you go to type the code, though, nothing appears on the display; instead, the keypad comes apart in your hands,
apparently having been smashed. Behind it is some kind of socket - one that matches a connector in your prototype
computer! You pull apart the smashed keypad and extract the logic circuit, plug it into your computer, and plug your
computer into the safe.

Now, you just need to figure out what output the keypad would have sent to the safe. You extract the assembunny code
from the logic chip (your puzzle input).
The code looks like it uses almost the same architecture and instruction set that the monorail computer used! You
should be able to use the same assembunny interpreter for this as you did there, but with one new instruction:

tgl x toggles the instruction x away (pointing at instructions like jnz does: positive means forward; negative
means backward):

For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
The arguments of a toggled instruction are not affected.
If an attempt is made to toggle an instruction outside the program, nothing happens.
If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that instruction,
skip it instead.
If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), the resulting instruction
is not executed until the next time it is reached.

For example, given this program:

cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a

cpy 2 a initializes register a to 2.
The first tgl a toggles an instruction a (2) away from it, which changes the third tgl a into inc a.
The second tgl a also modifies an instruction 2 away from it, which changes the cpy 1 a into jnz 1 a.
The fourth line, which is now inc a, increments a to 3.
Finally, the fifth line, which is now jnz 1 a, jumps a (3) instructions ahead, skipping the dec a instructions.
In this example, the final value in register a is 3.

The rest of the electronics seem to place the keypad entry (the number of eggs, 7) in register a, run the code, and
then send the value left in register a to the safe.

What value should be sent to the safe?
"""

# Refer to day 12

my_input = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""

with open('data/day23_input.txt', 'r') as f:
    my_input = f.read()

my_input = my_input.strip().split('\n')

def toggle(comm, proc_num):
    global my_input
    _, reg = comm.split(' ')
    val = registers[reg] + proc_num
    if val >= len(my_input):
        return
    newcomm = my_input[val].split(' ')
    if len(newcomm) == 2:
        if newcomm[0] == 'inc':
            my_input[val] = my_input[val].replace(newcomm[0], 'dec')
        else:
            my_input[val] = my_input[val].replace(newcomm[0], 'inc')
    else:
        if newcomm[0] == 'jnz':
            my_input[val] = my_input[val].replace(newcomm[0], 'cpy')
        else:
            my_input[val] = my_input[val].replace(newcomm[0], 'jnz')
    return

registers = {'a': 7, 'b': 0, 'c': 0, 'd': 0}

inst_len = len(my_input)
proc_num = 0

while proc_num < inst_len:
    comm = my_input[proc_num]

    if comm.startswith('cpy'):
        _, val, reg = comm.split(' ')
        try:
            registers[reg] = int(val)
        except ValueError:
            registers[reg] = registers[val]  # sometimes the copy is for a specific register rather than number
        except KeyError:  # if no register specified
            pass
        proc_num += 1
        continue
    elif comm.startswith('inc'):
        _, reg = comm.split(' ')
        registers[reg] += 1
        proc_num += 1
        continue
    elif comm.startswith('dec'):
        _, reg = comm.split(' ')
        registers[reg] -= 1
        proc_num += 1
        continue
    elif comm.startswith('jnz'):
        _, reg, val = comm.split(' ')
        try:
            val = int(val)
        except ValueError:
            val = registers[val]

        if reg in registers.keys():
            if registers[reg] == 0:
                proc_num += 1
            else:
                proc_num += val
        elif int(reg) > 0:
            proc_num += val
        else:
            proc_num += 1
        continue
    elif comm.startswith('tgl'):
        toggle(comm, proc_num)
        proc_num += 1


print(registers)

"""
--- Part Two ---

The safe doesn't open, but it does make several angry noises to express its frustration.

You're quite sure your logic is working correctly, so the only other thing is... you check the painting again. As
it turns out, colored eggs are still eggs. Now you count 12.

As you run the program with this new input, the prototype computer begins to overheat. You wonder what's taking so
long, and whether the lack of any instruction more powerful than "add one" has anything to do with it.
Don't bunnies usually multiply?

Anyway, what value should actually be sent to the safe?
"""

# Got some help from reddit:
# cpy b c
# inc a
# dec c
# jnz c -2
# dec d
# jnz d -5
# Basically sets a to be the product of b and d

registers = {'a': 12, 'b': 0, 'c': 0, 'd': 0}

inst_len = len(my_input)
proc_num = 0

while proc_num < inst_len:
    # Special modification to implement multiplication
    if proc_num == 4:
        registers['a'] = registers['b'] * registers['d']
        registers['c'] = 0
        registers['d'] = 0
        proc_num = 10
        continue

    comm = my_input[proc_num]

    if comm.startswith('cpy'):
        _, val, reg = comm.split(' ')
        try:
            registers[reg] = int(val)
        except ValueError:
            registers[reg] = registers[val]  # sometimes the copy is for a specific register rather than number
        except KeyError:  # if no register specified
            pass
        proc_num += 1
        continue
    elif comm.startswith('inc'):
        _, reg = comm.split(' ')
        registers[reg] += 1
        proc_num += 1
        continue
    elif comm.startswith('dec'):
        _, reg = comm.split(' ')
        registers[reg] -= 1
        proc_num += 1
        continue
    elif comm.startswith('jnz'):
        _, reg, val = comm.split(' ')
        try:
            val = int(val)
        except ValueError:
            val = registers[val]

        if reg in registers.keys():
            if registers[reg] == 0:
                proc_num += 1
            else:
                proc_num += val
        elif int(reg) > 0:
            proc_num += val
        else:
            proc_num += 1
        continue
    elif comm.startswith('tgl'):
        toggle(comm, proc_num)
        proc_num += 1

print(registers)

