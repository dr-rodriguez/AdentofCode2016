# Dec 4, 2016

"""
--- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms.
Of course, the list is encrypted and full of decoy data, but the instructions to decode the list
are barely hidden nearby. Better remove the decoy data first.

Each room consists of an encrypted name (lowercase letters separated by dashes) followed by a dash, a sector ID,
and a checksum in square brackets.

A room is real (not a decoy) if the checksum is the five most common letters in the encrypted name, in order,
with ties broken by alphabetization. For example:

aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters are a (5), b (3), and then a tie
between x, y, and z, which are listed alphabetically.
a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all tied (1 of each), the first
five are listed alphabetically.
not-a-real-room-404[oarel] is a real room.
totally-real-room-200[decoy] is not.
Of the real rooms from the list above, the sum of their sector IDs is 1514.

What is the sum of the sector IDs of the real rooms?
"""

import re
from collections import Counter
from operator import itemgetter  # to get specific item in tuple (since Counter return tuples of letter & frequency)

sum_ids = 0
with open('data/day4_input.txt') as f:
    for line in f:
        split_line = re.findall(r'\w+', line.strip())  # \w = [a-zA-Z0-9_] + = 1 or more
        checksum = split_line[-1]
        sector_id = int(split_line[-2])
        name = ''.join([s for s in split_line[:-2]])
        # print(name, sector_id, checksum)
        letters = Counter(name)

        # Sort alphabetically, then by reverse count
        five_letters = sorted(sorted(letters.items()), key=itemgetter(1), reverse=True)[:5]
        my_checksum = ''.join([s[0] for s in five_letters])
        # print(my_checksum, checksum)

        if checksum == my_checksum:
            sum_ids += sector_id

print('Answer: {}'.format(sum_ids))

"""
--- Part Two ---

With all the decoy data out of the way, it's time to decrypt this list and get moving.

The room names are encrypted by a state-of-the-art shift cipher, which is nearly unbreakable without the right
software. However, the information kiosk designers at Easter Bunny HQ were not expecting to deal with a master
cryptographer like yourself.

To decrypt a room name, rotate each letter forward through the alphabet a number of times equal to the room's
sector ID. A becomes B, B becomes C, Z becomes A, and so on. Dashes become spaces.

For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.

What is the sector ID of the room where North Pole objects are stored?
"""


def rotate_letters(word, sector_id):
    # Process a word to update each letter
    new_word = ''
    offset = 97  # so that ord('a')-offset = 0
    for letter in word:
        if letter == '-':
            new_word += ' '
            continue

        letter_num = ord(letter) - offset
        new_letter = chr((letter_num + sector_id) % 26 + offset)
        new_word += new_letter

    return new_word


with open('data/day4_input.txt') as f:
    for line in f:
        message = re.findall(r'[a-z\-]+', line.strip())[0]
        sector_id = int(re.findall(r'\d+', line.strip())[0])
        # print(message, sector_id)
        secret_message = rotate_letters(message, sector_id)

        # Tons of output, so just print out messages with 'north' in them
        if 'north' in secret_message:
            print('{} ({})'.format(secret_message, sector_id))

