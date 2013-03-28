import re
from string import ascii_letters, digits

def extractAlphanumeric(inputString):
    return "".join([ch for ch in inputString if ch in (ascii_letters + digits+" "+"-")])

def getKey(text):
    text1  = re.sub("[\.,  ,\?,:]", '-',extractAlphanumeric(text))
    text1  = re.sub("-+", '-', text1)
    text1  = text1.rstrip("-")
    return text1