import os
import sys
import random
import re
import json

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.escape import xhtml_unescape
from tornado.options import define, options

define("port", default=5000, help="run on the given port", type=int)

names = ['Nick', 'Steve', 'Andy', 'Qi', 'Fanny', 'Sarah', 'Cord', 'Todd',
    'Chris', 'Pasha', 'Gabe', 'Tony', 'Jason', 'Randal', 'Ali', 'Kim',
    'Rainer', 'Guillaume', 'Kelan', 'David', 'John', 'Stephen', 'Tom', 'Steven',
    'Jen', 'Marcus', 'Edy', 'Rachel']

humans_file = os.path.join(os.path.dirname(__file__), 'static', 'humans.txt')
messages_file = os.path.join(os.path.dirname(__file__), 'commit_messages.txt')
messages = {}

# Create a hash table of all commit messages
with open(messages_file) as messages_input:
    for line in messages_input.readlines():
        messages[md5(line).hexdigest()] = line

with open(humans_file) as humans_input:
    humans_content = humans_input.read()
    for line in humans_content.split("\n"):
        if "Name:" in line:
            data = line[6:].rstrip()
            if data.find("github:") == 0:
                names.append(data[7:])
            else:
                names.append(data.split(" ")[0])

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

class MainHandler(tornado.web.RequestHandler):
    def get(self, message_hash=None):
        if not message_hash:
            message_hash = random.choice(messages.keys())
        elif message_hash not in messages:
            raise tornado.web.HTTPError(404)

        message = fill_line(messages[message_hash])

        self.output_message(message, message_hash)

    def output_message(self, message, message_hash):
        self.render('index.html', message=message, message_hash=message_hash)

class PlainTextHandler(MainHandler):
    def output_message(self, message, message_hash):
        self.set_header('Content-Type', 'text/plain')
        self.write(xhtml_unescape(message).replace('<br/>', '\n'))

class JsonHandler(MainHandler):
    def output_message(self, message, message_hash):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps({'hash': message_hash, 'commit_message':message.replace('\n', ''), 'permalink': self.request.protocol + "://" + self.request.host + '/' + message_hash }))

class HumansHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write(humans_content)

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/([a-z0-9]+)', MainHandler),
    (r'/index.json', JsonHandler),
    (r'/([a-z0-9]+).json', JsonHandler),
    (r'/index.txt', PlainTextHandler),
    (r'/([a-z0-9]+)/index.txt', PlainTextHandler),
    (r'/humans.txt', HumansHandler),
], **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(os.environ.get("PORT", 5000))
    tornado.ioloop.IOLoop.instance().start()
