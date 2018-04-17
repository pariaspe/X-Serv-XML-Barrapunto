#!/usr/bin/python

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())

class CounterHandler(ContentHandler):

    def __init__ (self):
        self.inContent = 0
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            pass
            #self.title = normalize_whitespace(attrs.get('title'))
            #print(" item: " + self.title + ".")
        elif name == 'title':
            self.inContent = 1
        elif name == 'link':
            self.inContent = 1

    def endElement (self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)
        if name == 'item':
            print("")
        elif name == 'title':
            print("  title: " + self.theContent + ".")
        elif name == 'link':
            print("  link: " + self.theContent + ".")
        if self.inContent:
            self.inContent = 0
            self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

if len(sys.argv)<2:
    print("Usage: python xml-parser-jokes.py <document>")
    print()
    print(" <document>: file name of the document to parse")
    sys.exit(1)

# Load parser and driver

BarrapuntoParser = make_parser()
BarrapuntoHandler = CounterHandler()
BarrapuntoParser.setContentHandler(BarrapuntoHandler)

# Ready, set, go!

xmlFile = open(sys.argv[1],"r")
BarrapuntoParser.parse(xmlFile)

print("Parse complete")
