from email.parser import Parser
from os import path
from word import Word

import re

class Classifier(object):
    ''' Classifies email as spam or not spam using learned analyser '''
    def __init__(self, analyser):
        self.analyser = analyser
        
    def PrWS(self, word):
        try:
            return self.analyser.words[word].PrWS
        except KeyError:
            return 0.5      

    def PrWH(self, word):
        try:
            return self.analyser.words[word].PrWH
        except KeyError:
            return 0.5
            
            
    def PrSW(self, word):
        PrWS = self.PrWS(word)
        PrWH = self.PrWH(word)
        PrS = self.analyser.PrS
        PrH = self.analyser.PrH
        PrSW = (PrWS * PrS)/(PrWS * PrS + PrWH * PrH)
        return PrSW