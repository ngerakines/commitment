import os
import sys
import random
import tornado.httpserver
import tornado.ioloop
import tornado.web

names = ['Nick', 'Steve', 'Andy', 'Qi', 'Fanny', 'Sarah', 'Cord', 'Todd', 'Chris', 'Pasha', 'Gabe', 'Tony', 'Jason', 'Randal', 'Ali',  'Kim', 'Rainer']

def randline():
	text = 'commit_messages.txt'
	if not os.path.exists(text):
		return "Shit ..."
	f = file(text, 'rb')
	for i,j in enumerate(f):
		if random.randint(0,i) == i:
			line = j
	f.close()
	return line

def randname():
	for i,j in enumerate(names):
		if random.randint(0, i) == i:
			line = j
	return line

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		line = randline().replace("XNAMEX", randname())
		self.render("index.html", message = line)

class PlainTextHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "text/plain")
		line = randline().replace("XNAMEX", randname())
		self.write(line)

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/index.txt", PlainTextHandler),
], **settings)

if __name__ == "__main__":
	port = 8000
	if sys.argv[1]:
		port = int(sys.argv[1])
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()
