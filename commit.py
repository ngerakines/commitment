import os
import json
import signal

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.escape import xhtml_unescape
from tornado.options import define, options

import messages

define("port", default=5000, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self, message_hash=None):
        safe_only = self.get_argument("safe", default=False) != False
        censor = self.get_argument("censor", default=False)
        if censor == "":
            censor = True

        found_message = messages.find_by_md5(message_hash, censor=censor)

        if message_hash and not found_message:
            raise tornado.web.HTTPError(404)

        if found_message:
            self.output_message(found_message, message_hash)
        else:
            message, generated_message_hash = (
                messages.generate(safe_only=safe_only, censor=censor))
            self.output_message(message, generated_message_hash)

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
    port = os.environ.get("PORT", 5000)
    print("ready for requests (on port %s)" % (port))
    http_server.listen(port)
    tornado.ioloop.PeriodicCallback(application.try_exit, 100).start()
    tornado.ioloop.IOLoop.instance().start()
