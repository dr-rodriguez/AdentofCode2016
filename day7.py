# Dec 7, 2016

"""
--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP addresses
(they're IPv7, of course; IPv6 is much too limited). You'd like to figure out which
IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. An ABBA is any four-character sequence
which consists of a pair of two different characters followed by the reverse of that pair, such as xyyx or abba.
However, the IP also must not have an ABBA within any hypernet sequences, which are contained by square brackets.

For example:

abba[mnop]qrst supports TLS (abba outside square brackets).
abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).

How many IPs in your puzzle input support TLS?
"""

# import re
import regex as re  # using the new regex package for overlapped=True

"""
# Regex notes
test = 'tjwhvzwmhppijorvm[egqxqiycnbtxrii]ojmqyikithgouyu[lrllrgezaulugvlj]jdsrysawxkpglgg[mpvkikuabwucwlpqf]cmzkcdnrhwjmfgbmlq'
re.split(r'\[\w+\]', test)  # outside square brackets
re.findall(r'\[\w+\]', test)  # inside square brackets
test = 'abba[mnop]qrst'
test = 'abcd[bddb]xyyx'
test = 'ioxxoj[asdfgh]zxcvbn'
pattern = r'([a-z])([a-z])\2\1'
re.findall(pattern, test)  # grabs all, but only returns the () groups, not the full patterns
x = re.match(pattern, test)  # grab matches if the string starts with them
x = re.search(pattern, test)  # grabs first instance only
# Grabs all, allows iteration to get full pattern
x = re.finditer(pattern, test)
[s.group() for s in x]
"""

# This is a more elegant regex that will find abba and not aaaa
# abba_regex = r'(?!(\w)\1\1\1)(\w)(\w)\3\2'

def check_TLS(string):
    pattern = r'([a-z])([a-z])\2\1'
    t = re.search(pattern, string)
    if isinstance(t, type(None)):
        return False
    else:
        val = t.group()
        # Catch cases similar to aaaa, which are not valid
        if val[:2] == val[-2:]:
            return False
        else:
            return True

count = 0
with open('data/day7_input.txt') as f:
    for line in f:
        good = False
        bad = False

        supernet = re.split(r'\[\w+\]', line.strip())  # outside square brackets
        hypernet = re.findall(r'\[\w+\]', line.strip())  # inside square brackets

        supernet = '-'.join(supernet)
        good = check_TLS(supernet)

        hypernet = '-'.join(hypernet)
        bad = check_TLS(hypernet)
        if bad:
            good = False

        if good:
            count += 1

print('Answer: {}'.format(count))

"""
--- Part Two ---

You would also like to know which IPs support SSL (super-secret listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the supernet sequences
(outside any square bracketed sections), and a corresponding Byte Allocation Block, or BAB, anywhere in the
hypernet sequences. An ABA is any three-character sequence which consists of the same character twice with a
different character between them, such as xyx or aba. A corresponding BAB is the same characters but in
reversed positions: yxy and bab, respectively.

For example:

aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related,
because the interior character must be different).
zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz
and zbz overlap).

How many IPs in your puzzle input support SSL?
"""

count = 0
with open('data/day7_input.txt') as f:
    for line in f:
        good = False

        supernet = re.split(r'\[\w+\]', line.strip())  # outside square brackets
        hypernet = re.findall(r'\[\w+\]', line.strip())  # inside square brackets

        supernet = '-'.join(supernet)
        hypernet = '-'.join(hypernet)

        # Find all ABA cases and search for BAB cases in hypernet
        matches = re.finditer(r'(\w)(\w)\1', supernet, overlapped=True)  # need regex for overlapped parameter
        for entry in matches:
            val = entry.group()
            if val[0] == val[1]:  # to avoid cases like AAA
                continue

            # Make BAB from ABA
            newval = val[1:] + val[1]

            x = hypernet.find(newval)
            if x > 0:
                good = True
                break

        if good:
            count += 1

print('Answer: {}'.format(count))

