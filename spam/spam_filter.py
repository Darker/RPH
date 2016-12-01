from word import Word
from spam_analyser import Analyser
from spam_classifier import Classifier

class Filter(object):
    ''' Learns from messages and classifies unknown messages '''
    def __init__(self):
        

if __name__=="__main__":
    f = Filter()
    f.learn_all("./emails/1/!truth.txt")
