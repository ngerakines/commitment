import os
import sys
import random
import re
import json
import signal
from typing import Dict, List

from hashlib import md5

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.escape import xhtml_unescape
from tornado.options import define, options

define("port", default=5000, help="run on the given port", type=int)

humans_file = os.path.join(os.path.dirname(__file__), 'static', 'humans.txt')
messages_file = os.path.join(os.path.dirname(__file__), 'commit_messages.txt')
messages: Dict[str, str] = {}

# Create a hash table of all commit messages
with open(messages_file, 'r', encoding='utf-8') as messages_input:
    for line in messages_input.readlines():
        messages[md5(line.encode('utf-8')).hexdigest()] = line

names: List[str] = []

with open(humans_file, 'r', encoding='utf-8') as humans_input:
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
            message_hash = random.choice(list(messages.keys()))
        elif message_hash not in messages:
            raise tornado.web.HTTPError(404)

        message = fill_line(messages[message_hash])

        self.output_message(message, message_hash)

    def output_message(self, message, message_hash):
        self.set_header('X-Message-Hash', message_hash)
        self.render('index.html', message=message, message_hash=message_hash)

class PlainTextHandler(MainHandler):
    def output_message(self, message, message_hash):
        self.set_header('Content-Type', 'text/plain')
        self.set_header('X-Message-Hash', message_hash)
        self.write(xhtml_unescape(message).replace('<br/>', '\n'))

class JsonHandler(MainHandler):
    def output_message(self, message, message_hash):
        self.set_header('Content-Type', 'application/json')
        self.set_header('X-Message-Hash', message_hash)
        self.write(json.dumps({'hash': message_hash, 'commit_message':message.replace('\n', ''), 'permalink': self.request.protocol + "://" + self.request.host + '/' + message_hash }))

class HumansHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write(humans_content)

class CommitmentApplication(tornado.web.Application):
    is_closing = False

    def signal_handler(self, signum, frame):
        self.is_closing = True

    def try_exit(self):
        if self.is_closing:
            tornado.ioloop.IOLoop.instance().stop()

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

application = CommitmentApplication([
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
    signal.signal(signal.SIGINT, application.signal_handler)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(os.environ.get("PORT", 5000))
    tornado.ioloop.PeriodicCallback(application.try_exit, 100).start()
    tornado.ioloop.IOLoop.instance().start()
