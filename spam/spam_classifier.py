from email.parser import Parser
from os import path
from word import Word

import re

class Classifier(object):

    def __init__(self, parent):
        self.parent = parent
        

