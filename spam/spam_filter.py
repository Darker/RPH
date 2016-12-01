from word import Word
from spam_analyser import Analyser
from spam_classifier import Classifier

class Filter(object):
    ''' Learns from messages and classifies unknown messages '''
    def __init__(self):
    # opens file
    # if file is multipart message, calls learn_from message for 
    # HTML/TEXT content of message, HTML is preffered
    # if file is single part, just passes the message
    # to learn_from_message
    def wordlist_file(self, filename, is_spam):
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

    def wordlist_message(self, email, is_spam):
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
    def wordlist_text(self, text, is_spam):
        
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

if __name__=="__main__":
    f = Filter()
    f.learn_all("./emails/1/!truth.txt")
