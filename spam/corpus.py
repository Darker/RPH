from os import path
from email.parser import Parser
from utils import wordlist_file
import os
class Corpus(object):
    ''' Wrapper for reading from a directory. Not my idea. '''
    def __init__(self, path):
        self.dir = path
    def emails(self):
        for filename in os.listdir(self.dir):
            basename = path.basename(filename)
            if not basename.startswith("!"):
                # Opens file and parses email
                email = Parser().parse(open(filename, 'r', encoding="utf-8"))
                # For multipart emails, all bodies will be handled in a loop
                if email.is_multipart():
                    for msg in email.get_payload():
                        yield (filename, msg)
                else:
                    # Single part message is passed diractly
                    yield (filename, email)
    def wordlists(self):
        for filename in os.listdir(self.dir):
            basename = path.basename(filename)
            if not basename.startswith("!"):
                yield (filename, wordlist_file(path.join(self.dir, filename)))

