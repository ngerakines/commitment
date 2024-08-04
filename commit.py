import asyncio
import os
import random
import re
import json
from typing import Dict, List, Optional, Set

from hashlib import md5

import tornado.web
from tornado.escape import xhtml_unescape

default_names = [
    "Ali",
    "Andy",
    "April",
    "Brannon",
    "Chris",
    "Cord",
    "Dan",
    "Darren",
    "David",
    "Edy",
    "Ethan",
    "Fanny",
    "Gabe",
    "Ganesh",
    "Greg",
    "Guillaume",
    "James",
    "Jason",
    "Jay",
    "Jen",
    "John",
    "Kelan",
    "Kim",
    "Lauren",
    "Marcus",
    "Matt",
    "Matthias",
    "Mattie",
    "Mike",
    "Nate",
    "Nick",
    "Pasha",
    "Patrick",
    "Paul",
    "Preston",
    "Qi",
    "Rachel",
    "Rainer",
    "Randal",
    "Ryan",
    "Sarah",
    "Stephen",
    "Steve",
    "Steven",
    "Sunakshi",
    "Todd",
    "Tom",
    "Tony",
]

num_re = re.compile(r"XNUM([0-9,]*)X")


def fill_line(message: str, names: List[str]) -> str:
    message = message.replace("XNAMEX", random.choice(names))
    message = message.replace("XUPPERNAMEX", random.choice(names).upper())
    message = message.replace("XLOWERNAMEX", random.choice(names).lower())

    nums = num_re.findall(message)

    while nums:
        start = 1
        end = 999
        value = nums.pop(0) or str(end)
        if "," in value:
            position = value.index(",")
            if position == 0:  # XNUM,5X
                end = int(value[1:])
            elif position == len(value) - 1:  # XNUM5,X
                start = int(value[:position])
            else:  # XNUM1,5X
                start = int(value[:position])
                end = int(value[position + 1 :])
        else:
            end = int(value)
        if start > end:
            end = start * 2

        randint = random.randint(start, end)
        message = num_re.sub(str(randint), message, count=1)

    return message


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, messages: Dict[str, str], names: List[str]):
        self.messages = messages
        self.names = names

    def get(self, message_hash: Optional[str] = None):

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")
        self.set_header("Access-Control-Allow-Headers", "Origin,X-Requested-With,Content-Type,Accept")

        if message_hash is not None and message_hash not in self.messages:
            raise tornado.web.HTTPError(404)

        if message_hash is None:
            message_hash = random.choice(list(self.messages.keys()))

        message = fill_line(self.messages[message_hash], self.names)

        self.output_message(message, message_hash)

    def output_message(self, message, message_hash):
        self.set_header("X-Message-Hash", message_hash)
        self.render("index.html", message=message, message_hash=message_hash)


class PlainTextHandler(MainHandler):
    def output_message(self, message, message_hash):
        self.set_header("Content-Type", "text/plain")
        self.set_header("X-Message-Hash", message_hash)
        self.write(xhtml_unescape(message).replace("<br/>", "\n"))


class JsonHandler(MainHandler):
    def output_message(self, message, message_hash):
        self.set_header("Content-Type", "application/json")
        self.set_header("X-Message-Hash", message_hash)
        self.write(
            json.dumps(
                {
                    "hash": message_hash,
                    "commit_message": message.replace("\n", ""),
                    "permalink": f"{self.request.protocol}://{self.request.host}/{message_hash}",
                }
            )
        )


class HumansHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "text/plain")
        self.write(self.humans_content)


async def main():
    humans_file = os.path.join(os.path.dirname(__file__), "static", "humans.txt")
    messages_file = os.path.join(os.path.dirname(__file__), "commit_messages.txt")
    messages: Dict[str, str] = {}

    with open(messages_file, "r", encoding="utf-8") as messages_input:
        for line in messages_input.readlines():
            messages[md5(line.encode("utf-8")).hexdigest()] = line

    names: Set[str] = set(list(default_names))

    with open(humans_file, "r", encoding="utf-8") as humans_input:
        humans_content = humans_input.read()
        for line in humans_content.split("\n"):
            if "Name:" in line:
                line = line.removeprefix("Name: ")
                if (found := line.find("github")) > -1:
                    line = line[found:].removeprefix("github:").removesuffix(")")
                    names.add(line)
                else:
                    names.add(line.split(" ")[0])

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    values = {"messages": messages, "names": list(names)}
    application = tornado.web.Application(
        [
            (
                r"/(humans\.txt)",
                tornado.web.StaticFileHandler,
                dict(path=settings["static_path"]),
            ),
            (
                r"/(\.well\-known/openapi\.(yaml|json))",
                tornado.web.StaticFileHandler,
                dict(path=settings["static_path"]),
            ),
            
            (r"/", MainHandler, values),
            (r"/([a-z0-9]+)", MainHandler, values),
            (r"/index\.json", JsonHandler, values),
            (r"/([a-z0-9]+)\.json", JsonHandler, values),
            (r"/([a-z0-9]+)/index\.json", JsonHandler, values),
            (r"/index\.txt", PlainTextHandler, values),
            (r"/([a-z0-9]+)/index\.txt", PlainTextHandler, values),
            (r"/([a-z0-9]+)\.txt", PlainTextHandler, values),
        ],
        **settings,
    )
    application.listen(os.environ.get("PORT", 5000))
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
