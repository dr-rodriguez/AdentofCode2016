# Dec 20, 2016

"""
--- Day 20: Firewall Rules ---

You'd like to set up a small hidden computer here so you can use it to get back into the network later. However,
the corporate firewall only allows communication with certain external IP addresses.

You've retrieved the list of blocked IPs from the firewall, but the list seems to be messy and poorly maintained, and
it's not clear which IPs are allowed. Also, rather than being written in dot-decimal notation, they are written as
plain 32-bit integers, which can have any value from 0 through 4294967295, inclusive.

For example, suppose only the values 0 through 9 were valid, and that you retrieved the following blacklist:

5-8
0-2
4-7
The blacklist specifies ranges of IPs (inclusive of both the start and end value) that are not allowed. Then, the
only IPs that this firewall allows are 3 and 9, since those are the only numbers not in any range.

Given the list of blocked IPs you retrieved from the firewall (your puzzle input), what is the lowest-valued IP that
is not blocked?
"""

# my_input = """5-8
# 0-2
# 4-7"""
with open('data/day20_input.txt','r') as f:
    my_input = f.read()

lines = my_input.strip().split('\n')
lines = [(int(s.split('-')[0]), int(s.split('-')[1])) for s in lines]  # to sort by actual number and not string
lines.sort(reverse=False)

allpass = [False] * len(lines)
answer = 0
while not any(allpass):
    for i, line in enumerate(lines):
        l, u = line[0], line[1]

        allpass[i] = not l <= answer <= u
        # print('{} - ({}) - {} = {}'.format(l, answer, u, not l <= answer <= u))

        if not allpass[i]:
            if answer >= l:
                answer = u + 1
            else:
                answer = min(answer, max(l - 1, 0))

            allpass[i] = True
        else:
            continue

print('Answer: {}'.format(answer))

"""
--- Part Two ---

How many IPs are allowed by the blacklist?
"""

maxIP = 4294967295

count, ip, ind = 0, 0, 0
while ip < maxIP:
    l, u = lines[ind]
    if ip >= l:
        if ip <= u:
            ip = u + 1
            continue
        ind += 1
    else:
        count += 1
        ip += 1
print(count)

