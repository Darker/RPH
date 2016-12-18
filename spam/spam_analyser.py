from email.parser import Parser
from os import path
from word import Word
from utils import *
import math



class Analyser(object):
    ''' Analyses emails and creates statistical image word spamliness '''
    def __init__(self, parent):
        # Initialize memory of words
        # this will be map from word string to word class instance
        # This will contain:
        #   - links (only domain names though)
        #   - regular words - [a-z']
        #   - HTML tags, as <tagname>
        self.words = {}
        # This is similar to words, but remembers 
        # number of links in message and correlates them with it being spam
        #  not used yet because I dunno how to do the math
        self.link_counts = {}
        # probabilities that a message is or isn't spam
        self.PrS = 0.750814332247557
        self.PrH = 0.249185667752443
        self.p_treshold = 0.7
        
        self.emails = 0
        self.spams = 0
        self.hams = 0
        
        self.filter = parent
        
    def learn_all(self, truth_file):
        dirname = path.dirname(path.realpath(truth_file))
        print("Reading learning materials from '"+dirname+"'")
        spams = 0
        hams = 0
        with open(truth_file) as openfileobject:
            for line in openfileobject:
                info = line.split(" ")
                is_spam = not info[1].startswith("OK")
                if is_spam:
                    spams+=1
                else:
                    hams+=1
                self.learn_from_file(path.join(dirname, info[0]), is_spam)
                
        self.emails = spams + hams
        self.spams = spams
        self.hams = hams
                
        print("Dropping rare and boring words: ")
        common_words = ["a", "the", "you", "for", "if", "me", "us"]
        for word, stats in list(self.words.items()):
            if stats.occurences<5:
                del self.words[word]
                continue
            if math.fabs(stats.PrWS-0.5)<0.1:
                del self.words[word]
                continue
            if word in common_words:
                del self.words[word]
                continue
        
        print("Spams: ", spams)
        print("Hams: ", hams)
        self.PrS = spams/(spams+hams)
        # In this case, it's always much better to assume 
        # that a message is not spam
        if self.PrS>0.2:
            self.PrS=0.2
        self.PrH = 1-self.PrS
        print("PrS =", self.PrS)
        print("PrH =", self.PrH)
        print("\n")
        #self.nerdy_stats()
    def nerdy_stats(self):
        wordlist = self.words.values()
        print("Total words: ", len(wordlist)) 
        print("Most spammy words: ")
        
        sorted_by_spam = sorted(wordlist, key=lambda x: -x.spam+x.ham)
        
        it = 0
        for word in sorted_by_spam:
             word.printme()
             it+=1
             if it>20:
                 break   
        

    def learn_from_file(self, filename, is_spam):
        self.learn_from_list(wordlist_file(filename), is_spam)

    def learn_from_message(self, email, is_spam):
        self.learn_from_list(wordlist_message(email), is_spam)
    def learn_from_text(self, text, is_spam):
        self.learn_from_list(wordlist_text(text), is_spam)
    def learn_from_list(self, words, is_spam):
        for word in words:
            self.increment_word(word, is_spam)

    def increment_word(self, word, is_spam):
        try:
            self.words[word].increment(is_spam)
            #print("Incremented word "+word)
        except KeyError:
            self.words[word] = Word(word, is_spam)

