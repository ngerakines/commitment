import random
import re
import os
import sys

messages = open("commit_messages.txt").read().split('\n')

humans = open("static/humans.txt").read().split('\n')

names = ['Nick', 'Steve', 'Andy', 'Qi', 'Fanny', 'Sarah', 'Cord', 'Todd',
    'Chris', 'Pasha', 'Gabe', 'Tony', 'Jason', 'Randal', 'Ali', 'Kim',
    'Rainer', 'Guillaume', 'Kelan', 'David', 'John', 'Stephen', 'Tom', 'Steven',
    'Jen', 'Marcus', 'Edy', 'Rachel']

humans_file = os.path.join(os.path.dirname(__file__), 'static', 'humans.txt')

for line in open(humans_file).readlines():
    if "Name:" in line:
        data = line[6:].rstrip()
        if (data.find("github:") == 0):
            names.append(data[7:])
        else:
            names.append(data.split(" ")[0])

print "names", names

num_re = re.compile(r"XNUM([0-9,]*)X")

def fill_line(message):
    message = message.replace('XNAMEX', random.choice(names))
    message = message.replace('XUPPERNAMEX', random.choice(names).upper())
    message = message.replace('XLOWERNAMEX', random.choice(names).lower())

    nums = num_re.findall(message)

    while nums:
        start = 1
        end = 999
        value = nums.pop(0) or str(end)
        if "," in value:
            position = value.index(",")
            if position == 0: # XNUM,5X
                end = int(value[1:])
            elif position == len(value) - 1: # XNUM5,X
                start = int(value[:position])
            else: # XNUM1,5X
                start = int(value[:position])
                end = int(value[position+1:])
        else:
            end = int(value)
        if start > end:
            end = start * 2

        randint = random.randint(start, end)
        message = num_re.sub(str(randint), message, count=1)

    return message

def get(message=None):
    return fill_line(message or random.choice(messages))

if __name__ == '__main__':
    print get(sys.argv[1] or None)
