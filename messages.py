import os
import random
import re
from typing import Dict, List
from hashlib import md5
from itertools import cycle, islice

def generate(censor=False, safe_only=True):
    templates = safe_templates
    if censor:
        templates = safe_templates | censorable_templates
    elif not safe_only:
        templates = (unsafe_templates |
            safe_templates | censorable_templates)

    digest = _pick_random_key(templates)
    msg = _fill_template(templates[digest], censor=censor)
    return (msg, digest)

def find_by_md5(md5, censor=False):
    t = (unsafe_templates |
        safe_templates | censorable_templates).get(md5)

    if not t: return None

    return _fill_template(t, censor=censor)

this_file = os.path.dirname(__file__)
humans_file = os.path.join(this_file, 'static', 'humans.txt')

def _template_file(name):
    return os.path.join(this_file, 'commit_messages', name)

safe_templates_file = _template_file('safe.txt')
unsafe_templates_file = _template_file('unsafe.txt')
censorable_templates_file = _template_file('censorable.txt')

censorable_templates: Dict[str, str] = {}
safe_templates: Dict[str, str] = {}
unsafe_templates: Dict[str, str] = {}
names: List[str] = []

def _hash_template(template_text):
    return md5(template_text.encode('utf-8')).hexdigest()

def _hash_and_store(template_text, _dict):
    digest = _hash_template(template_text)
    _dict[digest] = template_text

print("hashing messages...")
with open(safe_templates_file, 'r', encoding='utf-8') as f:
    for line in f:
        _hash_and_store(line, safe_templates)
with open(unsafe_templates_file, 'r', encoding='utf-8') as f:
    for line in f:
        _hash_and_store(line, unsafe_templates)
with open(censorable_templates_file, 'r', encoding='utf-8') as f:
    for line in f:
        _hash_and_store(line, censorable_templates)

def check_for_collisions():
    all_template_digests = (list(safe_templates.keys()) +
        list(unsafe_templates.keys()) +
        list(censorable_templates.keys()))
    if len(all_template_digests) != len(set(all_template_digests)):
        raise Exception("uniqueness problem with source data")
check_for_collisions()

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

def _fill_template(txt, censor=False):
    txt = txt.replace('XNAMEX', random.choice(names))
    txt = txt.replace('XUPPERNAMEX', random.choice(names).upper())
    txt = txt.replace('XLOWERNAMEX', random.choice(names).lower())
    if censor:
        txt = _censor_swearing(txt, censor=censor)

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

SWEARING = [
    "refuckulated", # funnier censored
    "motherfucker",
    "cocksucker",
    "bollocks", # may be safe but funnier/safer censored
    "fucking",
    "cunts",
    "fuck",
    "shit",
    "damn", # also funnier censored
]
# https://en.wikipedia.org/wiki/Grawlix
GRAWLIX = "!@#$%&*"

def _censor_swearing(txt, censor=False):
    grawlix_chars = censor if type(censor) == str else GRAWLIX
    grawlix_chars = list(grawlix_chars)

    for swearword in SWEARING:
        random.shuffle(grawlix_chars)

        grawlix = "".join(list(islice(cycle(grawlix_chars), len(swearword))))
        txt = re.sub(swearword, grawlix, txt, flags=re.IGNORECASE)
    return txt
