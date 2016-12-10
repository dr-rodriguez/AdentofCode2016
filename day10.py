# Dec 10, 2016

"""
--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing small microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it has two microchips, and once it does,
it gives each one to a different bot or puts it in a marked "output" bin. Sometimes, bots take microchips from
"input" bins, too.

Inspecting one of the microchips, it seems like they each contain a single number; the bots must use some logic to
decide what to do with each chip. You access the local control computer and download the bots' instructions
(your puzzle input).

Some of the instructions specify that a specific-valued microchip should be given to a specific bot; the rest of the
instructions indicate what a given bot should do with its lower-value or higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2 chip and a value-5 chip.
Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.
In the end, output bin 0 contains a value-5 microchip, output bin 1 contains a value-2 microchip, and output bin 2
contains a value-3 microchip. In this configuration, bot number 2 is responsible for comparing value-5 microchips with
value-2 microchips.

Based on your instructions, what is the number of the bot that is responsible for comparing value-61 microchips
with value-17 microchips?
"""

import re
import numpy as np


def process_instruction(my_input):
    # Attempt to process instructions and store to global variables
    # If good return True, otherwise return False
    global bots
    global outputs

    if my_input.startswith('value'):
        pattern = r'value (\d+) goes to bot (\d+)'
        chip, bot_num = re.findall(pattern, my_input)[0]
        chip = int(chip)
        # Attempt to add input
        check = add_to_bot(bot_num, chip)
        if check:
            return True
        else:
            return False
    else:
        pattern = r'bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)'
        bot_num, out1, val1, out2, val2 = re.findall(pattern, my_input)[0]
        # Check existence of bot and bot's hand
        if bot_num not in bots.keys():
            return False
        check_len = len(bots[bot_num])
        if check_len <= 1:
            return False
        else:
            hand = np.sort([bots[bot_num].pop(), bots[bot_num].pop()])

            # Output message for part 1 answer
            t1 = 17
            t2 = 61
            if hand[0] == t1 and hand[1] == t2:
                print("Bot {} has chips {} and {}".format(bot_num, t1, t2))

            check1 = hand_over(out1, val1, hand[0])
            check2 = hand_over(out2, val2, hand[1])
            if check1 and check2:
                return True
            else:
                return False


def add_to_bot(bot_num, chip):
    # Add chip to a bot
    global bots

    # Test if bot exists already, otherwise create it
    if bot_num not in bots.keys():
        bots[bot_num] = list()

    # Test if bot contains an entry already
    check_len = len(bots[bot_num])
    if check_len <= 1:
        bots[bot_num].append(chip)
        return True
    if check_len >= 2:
        # Can't hold another chip
        return False


def hand_over(outname, out, value):
    # Hand over a value to another bot or the output
    global outputs
    global bots

    if outname == 'output':
        # Check existence, otherwise create
        if out not in outputs:
            outputs[out] = list()
        outputs[out].append(value)
        return True
    else:
        if out not in bots:
            bots[out] = list()
        check_len = len(bots[out])
        if check_len <= 1:
            bots[out].append(value)
            return True
        else:
            return False


with open('data/day10_input.txt') as f:
    my_input = f.read().split('\n')

bots = dict()
outputs = dict()

while len(my_input) > 0:
    my_input = [s for s in my_input if not process_instruction(s)]

"""
--- Part Two ---

What do you get if you multiply together the values of one chip in each of outputs 0, 1, and 2?
"""

answer = outputs['0'][0] * outputs['1'][0] * outputs['2'][0]
print('Answer: {}'.format(answer))
