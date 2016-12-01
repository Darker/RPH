from email.parser import Parser
from os import path
from word import Word

import re
HTML_ENDTAG = re.compile(r"<\s*/[a-z]+\s*>")
URL = re.compile(r"https?://(www\.)?([^\s/\?@\">]+)[^\s\">]*")
HTML_OPENTAG = re.compile(r"<([a-z]+)([^>a-z][^>]*|\s*/)?>")
ENTITIES = re.compile(r"\&[a-z0-9]+\;")
GARBAGE = re.compile(r"([^a-z-' ]|([^a-z]|^)[-' ]([^a-z]|$))")
WORD = re.compile(r"([a-z]+([-'][a-z]+)?)")

class Analyser(object):
    ''' Analyses emails and creates statistical image word spamliness '''
    def __init__(self):
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
        print("Spams: ", spams)
        print("Hams: ", hams)
        self.PrS = spams/(spams+hams)
        self.PrH = hams/(spams+hams)
        print("PrS =", self.PrS)
        print("PrH =", self.PrH)
        self.nerdy_stats()
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
        
    # opens file
    # if file is multipart message, calls learn_from message for 
    # HTML/TEXT content of message, HTML is preffered
    # if file is single part, just passes the message
    # to learn_from_message
    def learn_from_file(self, filename, is_spam):
        # Opens file and parses email
        email = Parser().parse(open(filename, 'r'))
        email.filename = filename
        # For multipart emails, all bodies will be handled in a loop
        if email.is_multipart():
            for msg in email.get_payload():
                msg.filename = filename
                self.learn_from_message(msg, is_spam)
        else:
            # Single part message is passed diractly
            self.learn_from_message(email, is_spam)

    def learn_from_message(self, email, is_spam):
        payload = email.get_payload(decode=True)
        if payload is None:
            print("Error - no body in "+email.filename)
            return
        # The payload is binary. It must be converted to
        # python string depending in input charset
        # Input charset may vary, based on message
        try:
            text = payload.decode("utf-8")
            self.learn_from_text(text, is_spam)
        except UnicodeDecodeError:
            print("Error: cannot parse message "+email.filename+" as UTF-8")
            return  
        #print(text.encode("utf-8"))
        #raise ValueError("Fuck it I'm goin' home.")
    def learn_from_text(self, text, is_spam):
        
        text = text.lower()
        text = text.replace("\n", "")
        text = HTML_ENDTAG.sub("", text)
        # Remember all link domains mentioned here:
        for link in URL.finditer(text):
            #print("Matched link: ", link.group(0), " - domain:"+link.group(2))
            self.increment_word("URL:"+link.group(2), is_spam)
        # remove the links
        text = URL.sub("", text)
        # remember all HTML tags
        for link in HTML_OPENTAG.finditer(text):
            #print("Matched HTML tag: <"+link.group(1)+">")
            self.increment_word("<"+link.group(1)+">", is_spam)
        # remove the tags
        text = HTML_OPENTAG.sub("", text)
        original_text = text
        text = ENTITIES.sub("", text)
        # clean the remaining garbage away:
        text = GARBAGE.sub(" ", text)
        for word in WORD.finditer(text):
            #print("Matched word: "+word.group(1))
            self.increment_word(word.group(1), is_spam)
            if False and word.group(1)=="nbsp":
                print("\nORIGINAL TEXT:\n\n")
                print(original_text)
                print("\nFINAL TEXT:\n\n")
                print(text)
                raise ValueError("Invalid parsing.")
    def increment_word(self, word, is_spam):
        try:
            self.words[word].increment(is_spam)
            #print("Incremented word "+word)
        except KeyError:
            self.words[word] = Word(word, is_spam)

if __name__=="__main__":
    f = Filter()
    f.learn_all("./emails/1/!truth.txt")
