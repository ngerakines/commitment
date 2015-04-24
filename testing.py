import random
import re

messages = open("commit_messages.txt").read().split('\n')

names = ['Nick', 'Steve', 'Andy', 'Qi', 'Fanny', 'Sarah', 'Cord', 'Todd',
    'Chris', 'Pasha', 'Gabe', 'Tony', 'Jason', 'Randal', 'Ali', 'Kim',
    'Rainer', 'Guillaume', 'Kelan', 'David', 'John', 'Stephen', 'Tom', 'Steven',
    'Jen', 'Marcus', 'Edy', 'Rachel']

def get(message=None):
    message = message or random.choice(messages)

    message = message.replace('XNAMEX', random.choice(names))
    message = message.replace('XUPPERNAMEX', random.choice(names).upper())
    message = message.replace('XLOWERNAMEX', random.choice(names).lower())
    
    num_re = re.compile(r"XNUM([0-9]*),?([0-9]*)X")
    nums = num_re.findall(message)

    while nums:
        start, end = nums.pop(0)

        if start and end:
            #yay, everything was given
            start, end = map(int, (start, end))
            start, end = min(start, end), max(start, end)  #silly XNAMEX

            if start == end:
                #what the fuck are you even doing
                randint = start
            else:
                randint = random.randint(start, end)
        elif (start and not end) or (end and not start):
            #only one bound was given
            #either way, consider it the upper bound
            num = int(start or end)
            
            #edge-case when start or end is 0
            #this doesn't do negatives though so wtf XNAMEX?
            randint = 0 if not num else random.randint(1, num)
        else:
            #no bounds given, so we assume that the message wants a random
            #integer between 1 and 999 inclusive. If the message wants
            #something different, it should specify that!
            #My logic here is that this is the normal need
            randint = random.randint(1, 999)

        #only do one replacement, to allow multiple XNUMX's
        message = num_re.sub(str(randint), message, count=1)

    return message
