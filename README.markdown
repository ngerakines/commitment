# Looking For Sponsors

Enjoying https://whatthecommit.com/ ? Consider becoming a sponsor of this project. Your contributions keep the site running.

https://github.com/users/ngerakines/sponsorship

# About WTC (What The Commit)
Commitment is a small Tornado application that generates random commit messages.

    https://whatthecommit.com/

Commitment also provides https://whatthecommit.com/index.txt which provides plain text output.  
Some interesting usage for that can be:
```
git config --global alias.yolo '!git commit -m "$(curl -s https://whatthecommit.com/index.txt)"'
```

## Make it safe for work

    https://whatthecommit.com/?safe filters out any unsafe or swearing messages
    https://whatthecommit.com/?censor censors them instead, and filters messages that wouldn't be funny if censored
    https://whatthecommit.com/?censor=* censors using custom pattern

Or use one of the following VSCode Extensions:

- [WhatTheCommit](https://marketplace.visualstudio.com/items?itemName=Gaardsholt.vscode-whatthecommit) 
- [yoloCommit](https://marketplace.visualstudio.com/items?itemName=JohnStilia.yolocommit)

# License

Copyright (c) 2010-2021 Nick Gerakines <nick@gerakines.net>

This project and its contents are open source under the MIT license.
