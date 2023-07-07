these are the source text files from which all the commit messages
are generated

- put commit messages with swear words in censorable.txt, this makes
them funny by using [grawlixes](https://en.wikipedia.org/wiki/Grawlix)

- put other nsfw in unsafe, because they cannot be made funny and safe
by using grawlixes

- put safe for work messages in safe.txt.

## Script for filtering of swear words

This was used to create the initial list of unsafe words.

```py
BAD_WORDS = [
    "shit",
    "piss",
    "fuck",
    "cunt",
    "cocksucker",
    "motherfucker",
    "tits",

    "cock",
    "fucker",

    "fart",
    "turd",
    "twat",

    "dicksucker",
    "fucking",

    "sex",
    "sexy",
]

safe_f = open("commit_messages/safe.txt", "w")
unsafe_f = open("commit_messages/unsafe.txt", "w")

with open("./commit_messages.txt") as original_f:
    for line in original_f:
        bad = False

        for bad_word in BAD_WORDS:
            if bad_word in line.lower():
                bad = True

        if bad:
            unsafe_f.write(line)
        else:
            safe_f.write(line)

safe_f.close()
unsafe_f.close()
```
