from email.parser import Parser
    
def read_classification_from_file(truth_file):
    classifications = {}
    with open(truth_file, encoding="utf-8") as openfileobject:
        for line in openfileobject:
            info = line.replace("\n", "").split(" ")
            classifications[info[0]] = info[1]
    return classifications


# Returns list of words in mail file
def wordlist_file(filename, duplicities=True):
    # Opens file and parses email
    email = Parser().parse(open(filename, 'r', encoding="utf-8"))
    email.filename = filename
    # For multipart emails, all bodies will be handled in a loop
    if email.is_multipart():
        words = []
        for msg in email.get_payload():
            msg.filename = filename
            # add list of words from this body to the rest
            words += wordlist_message(msg, duplicities)
        return words;
    else:
        # Single part message is passed diractly
        return wordlist_message(email, duplicities)
# Returns list of words in single email object
def wordlist_message(email, duplicities=True):
    payload = email.get_payload(decode=True)
    if payload is None:
        print("Error - no body in "+email.filename)
        return []
    # The payload is binary. It must be converted to
    # python string depending in input charset
    # Input charset may vary, based on message
    try:
        text = payload.decode("utf-8")
        #self.learn_from_text(text, is_spam)
        return wordlist_text(text, duplicities)
    except UnicodeDecodeError:
        print("Error: cannot parse message "+email.filename+" as UTF-8")
        return []
        
import re
HTML_ENDTAG = re.compile(r"<\s*/[a-z]+\s*>")
URL = re.compile(r"https?://(www\.)?([^\s/\?@\">]+)[^\s\">]*")
HTML_OPENTAG = re.compile(r"<([a-z]+)([^>a-z][^>]*|\s*/)?>")
ENTITIES = re.compile(r"\&[a-z0-9]+\;")
GARBAGE = re.compile(r"([^a-z-' ]|([^a-z]|^)[-' ]([^a-z]|$))")
WORD = re.compile(r"([a-z]+([-'][a-z]+)?)")
def wordlist_text(text, duplicities=True):
    words = []
    text = text.lower()
    text = text.replace("\n", "")
    text = HTML_ENDTAG.sub("", text)
    # Remember all link domains mentioned here:
    for link in URL.finditer(text):
        #print("Matched link: ", link.group(0), " - domain:"+link.group(2))
        #self.increment_word("URL:"+link.group(2), is_spam)
        word = "URL:"+link.group(2)
        if duplicities or not(word in words):
           words.append(word)
    # remove the links
    text = URL.sub(" ", text)
    # remember all HTML tags
    for link in HTML_OPENTAG.finditer(text):
        #print("Matched HTML tag: <"+link.group(1)+">")
        #self.increment_word("<"+link.group(1)+">", is_spam)
        word = "<"+link.group(1)+">"
        if duplicities or not(word in words):
           words.append(word)
    # remove the tags
    text = HTML_OPENTAG.sub(" ", text)
    original_text = text
    text = ENTITIES.sub(" ", text)
    # clean the remaining garbage away:
    text = GARBAGE.sub(" ", text)
    for word in WORD.finditer(text):
        #print("Matched word: "+word.group(1))
        #self.increment_word(word.group(1), is_spam)
        word = word.group(1)
        if duplicities or not(word in words):
           words.append(word)
    return words;