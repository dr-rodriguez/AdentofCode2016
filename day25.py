# Dec 25, 2016

"""
--- Day 25: Clock Signal ---

You open the door and find yourself on the roof. The city sprawls away from you for miles and miles.

There's not much time now - it's already Christmas, but you're nowhere near the North Pole, much too far to deliver
these stars to the sleigh in time.

However, maybe the huge antenna up here can offer a solution. After all, the sleigh doesn't need the stars, exactly;
it needs the timing data they provide, and you happen to have a massive signal generator right here.

You connect the stars you have to your prototype computer, connect that to the antenna, and begin the transmission.

Nothing happens.

You call the service number printed on the side of the antenna and quickly explain the situation. "I'm not sure what
kind of equipment you have connected over there," he says, "but you need a clock signal." You try to explain that
this is a signal for a clock.

"No, no, a clock signal - timing information so the antenna computer knows how to read the data you're sending it. An
endless, alternating pattern of 0, 1, 0, 1, 0, 1, 0, 1, 0, 1...." He trails off.

You ask if the antenna can handle a clock signal at the frequency you would need to use for the data from the stars.
"There's no way it can! The only antenna we've installed capable of that is on top of a top-secret Easter Bunny
installation, and you're definitely not-" You hang up the phone.

You've extracted the antenna's clock signal generation assembunny code (your puzzle input); it looks mostly compatible
with code you worked on just recently.

This antenna code, being a signal generator, uses one extra instruction:

out x transmits x (either an integer or the value of a register) as the next value for the clock signal.
The code takes a value (via register a) that describes the signal to generate, but you're not sure how it's used.
You'll have to find the input to produce the right signal through experimentation.

What is the lowest positive integer that can be used to initialize register a and cause the code to output a clock
signal of 0, 1, 0, 1... repeating forever?
"""



with open('data/day25_input.txt') as f:
    my_input = f.read().strip().split('\n')


def proc_inst(proc_num):
    global my_input
    global registers
    comm = my_input[proc_num]

    if comm.startswith('cpy'):
        _, val, reg = comm.split(' ')
        try:
            registers[reg] = int(val)
        except ValueError:
            registers[reg] = registers[val]  # sometimes the copy is for a specific register rathern than number
        proc_num += 1
    elif comm.startswith('inc'):
        _, reg = comm.split(' ')
        registers[reg] += 1
        proc_num += 1
    elif comm.startswith('dec'):
        _, reg = comm.split(' ')
        registers[reg] -= 1
        proc_num += 1
    elif comm.startswith('jnz'):
        _, reg, val = comm.split(' ')
        if reg in registers.keys():
            if registers[reg] == 0:
                proc_num += 1
            else:
                proc_num += int(val)
        elif int(reg) > 0:
            proc_num += int(val)
        else:
            proc_num += 1

    return proc_num

inst_len = len(my_input)
for i in range(0, 1000):
    registers = {'a': i, 'b': 0, 'c': 0, 'd': 0, 'out': [1]}
    # print(registers)
    proc_num = 0
    count = 0
    max_len = 1000
    # good = True
    while proc_num < inst_len and count < max_len:
        comm = my_input[proc_num]

        if comm.startswith('out'):
            _, reg = comm.split(' ')

            if registers[reg] not in (0, 1) or registers[reg] == registers['out'][-1]:
                break
            else:
                registers['out'] += [registers[reg]]
                # print('{}: {} {}'.format(i, registers['out'], count))

            proc_num += 1
            count += 1
        else:
            proc_num = proc_inst(proc_num)

    if len(registers['out']) > 2 and len(registers['out']) >= max_len:
        out = ''.join(['{}'.format(s) for s in registers['out'][1:]])
        print('{}: {}'.format(i, out))

# This works after fixing some bugs

# Trying to manually figure out my input, with help from reddit
"""
cpy a d
cpy 4 c
cpy 643 b
d = a, b = 643, c = 4
{
inc d
dec b
jnz b -2
dec c
jnz c -5
}
d = d + b*c aka:
d = a + 4*643
cpy d a     ** a = d
jnz 0 0     *
{
cpy a b     b = a
cpy 0 a     a = 0
cpy 2 c     c = 2
jnz b 2     if b>0: { b--, c--  --> c = 2 - (b % c) = 2 - (a % 2)
jnz 1 6     else: >>
dec b
dec c       }
jnz c -4    if c>0: back to jnz b 2
inc a       a++
jnz 1 -7    back to cpy 2 c
cpy 2 b     << b = 2
jnz c 2     if c>0: { b--, c--
jnz 1 4     else: >>>
dec b
dec c
jnz 1 -4    } back to jnz c 2
jnz 0 0     <<<
out b
}
jnz a -19   if a>0: back to *
jnz 1 -21   back to **
"""

for a1 in range(157, 159):
    d = a1 + (4 * 643)
    out = []
    for i in range(0, 100):
        a = d
        while a != 0:
            c = 2 - (a % 2)
            a //= 2  # integer division
            b = 2 - c
            out.append(b)
    print('{}: {}'.format(a1, ''.join(['{}'.format(s) for s in out])))
