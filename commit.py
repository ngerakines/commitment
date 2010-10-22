import os
import sys
import random
import tornado.httpserver
import tornado.ioloop
import tornado.web

names = ['Nick', 'Steve', 'Andy', 'Qi', 'Fanny', 'Sarah', 'Cord', 'Todd',
    'Chris', 'Pasha', 'Gabe', 'Tony', 'Jason', 'Randal', 'Ali', 'Kim',
    'Rainer', 'Guillaume']

messages_file = os.path.join(os.path.dirname(__file__), 'commit_messages.txt')
messages = open(messages_file).readlines()

def randname():
    return random.choice(names)

def randmessage():
    return random.choice(messages)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        message = randmessage().replace("XNAMEX", randname())
        self.output_message(message)

    def output_message(self, message):
        self.render('index.html', message=message)

class PlainTextHandler(MainHandler):
    def output_message(self, message):
        self.set_header('Content-Type', 'text/plain')
        self.write(message)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/index.txt", PlainTextHandler),
], **settings)

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
