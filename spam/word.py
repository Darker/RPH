from bcolors import bcolors as ANSI
class Word(object):
    '''Describes a word found in emails, and with what probabilities'''
    def __init__(self, word, is_spam=None):
        self.occurences = 0
        self.spam = 0
        self.ham = 0
        self.word = word
        if is_spam is not None:
            self.increment(is_spam)
    
    def increment(self, is_spam):
        self.occurences += 1
        if is_spam:
            self.spam += 1
        else:
            self.ham += 1
    @property
    def spam_prob(self):
        return self.spam/self.occurences
    @property
    def ham_prob(self):
        return self.ham/self.occurence
        
    def printme(self):
        print(self.word + " ("+str(self.occurences)+" | "+ANSI.RED+str(self.spam)+ANSI.RESET+" | "+ANSI.GREEN+str(self.ham)+ANSI.RESET+")")