import os
import sys
import random

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.escape import xhtml_unescape

names = ['Nick', 'Steve', 'Andy', 'Qi', 'Fanny', 'Sarah', 'Cord', 'Todd',
    'Chris', 'Pasha', 'Gabe', 'Tony', 'Jason', 'Randal', 'Ali', 'Kim',
    'Rainer', 'Guillaume', 'Kelan', 'David', 'John', 'Stephen']

messages_file = os.path.join(os.path.dirname(__file__), 'commit_messages.txt')
messages = {}

# Create a hash table of all commit messages
for line in open(messages_file).readlines():
    messages[md5(line).hexdigest()] = line

class MainHandler(tornado.web.RequestHandler):
    def get(self, message_hash=None):
        if not message_hash:
            message_hash = random.choice(messages.keys())
        elif message_hash not in messages:
            raise tornado.web.HTTPError(404)

        message = messages[message_hash].replace(
            'XNAMEX', random.choice(names))

        message = message.replace('XUPPERNAMEX', random.choice(names).upper())
        message = message.replace('XLOWERNAMEX', random.choice(names).lower())

        self.output_message(message, message_hash)

    def output_message(self, message, message_hash):
        self.render('index.html', message=message, message_hash=message_hash)

class PlainTextHandler(MainHandler):
    def output_message(self, message, message_hash):
        self.set_header('Content-Type', 'text/plain')
        self.write(xhtml_unescape(message).replace('<br/>', '\n'))

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/([a-z0-9]+)', MainHandler),
    (r'/index.txt', PlainTextHandler),
    (r'/([a-z0-9]+)/index.txt', PlainTextHandler),
], **settings)

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
