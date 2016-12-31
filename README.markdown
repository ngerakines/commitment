Commitment is a small Tornado application that generates random commit messages.

    http://whatthecommit.com/

Commitment also provides http://whatthecommit.com/index.txt which provides plain text output.  
Some interesting usage for that can be:
```
git config --global alias.yolo '!git commit -m "$(curl -s whatthecommit.com/index.txt)"'
```

# License

Copyright (c) 2017 Nick Gerakines <nick@gerakines.net>

This project and its contents are open source under the MIT license.

