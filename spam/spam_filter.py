from __future__ import print_function
from word import Word
from spam_analyser import Analyser
from spam_classifier import Classifier
from email.parser import Parser
from os import path

from utils import *
from corpus import Corpus

class Filter(object):
    ''' Learns from messages and classifies unknown messages '''
    def __init__(self):
        self.analyser = Analyser(self)
        self.classifier = Classifier(self.analyser)
        
    
    def train(self, directory):
        truth_file = path.join(directory, "!truth.txt")
        if path.isfile(truth_file):
            self.analyser.learn_all(truth_file)
        else:
           raise ValueError("Invalid path to corpus directory, truth file not found.")
    def test(self, directory):
        c = Corpus(directory)
        with open(path.join(directory, "!prediction.txt"), 'w', encoding="utf-8") as output:
            for (filename, wordlist) in c.wordlists():
                prob_spam = self.classifier.prob_list(wordlist)
                is_spam = prob_spam>=self.analyser.p_treshold
                tag = "SPAM" if is_spam else "OK"
                output.write(filename+" "+tag+"\n")

if __name__=="__main__":
    f = Filter()
    f.train("./emails/2/")
    print("Prob for unknown word: ", f.classifier.PrSW("dsgfdgf"))
    print("Prob for spam word: ", f.classifier.PrSW("<br>"))
    print("Prob for 'URL:geocities.com': ", f.classifier.PrSW("URL:geocities.com"))

    f.test("./emails/1/")
    
