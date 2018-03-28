from email.parser import Parser
from os import path
from word import Word 
from utils import *

import re
import math

class Classifier(object):
    ''' Classifies email as spam or not spam using learned analyser '''
    def __init__(self, analyser):
        self.analyser = analyser
    # robability that a file is spam
    def prob_file(self, filename):
        words = wordlist_file(filename)
    # probability that a list of words is spam
    def prob_list(self, words):
        # if mail fails to parse, return as if it was ham
        if len(words)==0:
            return 0
        n = 0
        for word in words:
            pi = self.PrSW(word)
            # print("pi=", pi)
            if pi==1.0:
                #print("Word:", word, " 100% spam...")
                pi = 0.999999
            if pi==0.0:
                #print("Word:", word, " 0% spam...")
                pi = 0.00001
            try:
                n+= math.log(1-pi)-math.log(pi)
            except ValueError:
                print("Word:", word, " stats: ", n, "  ", pi)
                raise ValueError("Wtf man!")
            #multiply*=pr
            #negative_multiply*=(1-pr)
        try:
            return 1/(1+math.e**n)
        except OverflowError:
            return 0
            
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