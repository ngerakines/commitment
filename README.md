# Commitment
Commitment is a small Tornado application that generates random commit messages.  
[whatthecommit.com](http://whatthecommit.com/)

## Plain Text
Commitment also provides plain text output [here](http://whatthecommit.com/index.txt).  
Some interesting usage for that can be:
```
git config --global alias.yolo '!git commit -m "$(curl -s whatthecommit.com/index.txt)"'
```

## License
This project and its contents are open source under the MIT license.  
Copyright (c) 2010-2017 Nick Gerakines <nick@gerakines.net>
