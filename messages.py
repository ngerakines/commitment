import os
import random
import re
from typing import Dict, List
from hashlib import md5

def generate():
    digest = _pick_random_key(templates)
    msg = templates[digest]
    return (msg, digest)

def find_by_md5(md5):
    if md5 not in templates:
        return None
    else:
        t = templates[md5]
        return _fill_template(t)

this_file = os.path.dirname(__file__)
humans_file = os.path.join(this_file, 'static', 'humans.txt')
all_messages_file = os.path.join(this_file, 'commit_messages.txt')
tmp = os.path.join(this_file, 'tmp')
os.makedirs(tmp, exist_ok=True)

templates: Dict[str, str] = {}
names: List[str] = []

# Create a hash table of all commit message templates
print("hashing messages...")
with open(all_messages_file, 'r', encoding='utf-8') as f:
    for line in f:
        templates[md5(line.encode('utf-8')).hexdigest()] = line

with open(humans_file, 'r', encoding='utf-8') as f:
    for line in f:
        if "Name:" in line:
            data = line[6:].rstrip()
            if data.find("github:") == 0:
                names.append(data[7:])
            else:
                names.append(data.split(" ")[0])

def _pick_random_key(templates):
    return random.choice(list(templates.keys()))

num_re = re.compile(r"XNUM([0-9,]*)X")

def _fill_template(txt):
    txt = txt.replace('XNAMEX', random.choice(names))
    txt = txt.replace('XUPPERNAMEX', random.choice(names).upper())
    txt = txt.replace('XLOWERNAMEX', random.choice(names).lower())

    nums = num_re.findall(txt)

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
        txt = num_re.sub(str(randint), txt, count=1)

    return txt
