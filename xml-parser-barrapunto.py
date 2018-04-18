#!/usr/bin/python

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string
import os
from urllib import request

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())

class CounterHandler(ContentHandler):

    def __init__ (self):
        self.inContent = 0
        self.theContent = ""
        self.inItem = False

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = 1
            elif name == 'link':
                self.inContent = 1

    def endElement (self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)
        if name == 'item':
            self.inItem = False
            print('</br>', file=open("barrapunto.html", "a"))
        if self.inItem:
            if name == 'title':
                print(self.theContent, file=open("barrapunto.html", "a"))
            elif name == 'link':
                print('<a href="' + self.theContent + '">' + self.theContent + '</a>', file=open("barrapunto.html", "a"))
        if self.inContent:
            self.inContent = 0
            self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

if len(sys.argv)<1:
    print("Usage: python xml-parser-barrapunto.py")
    print()
    sys.exit(1)

# Delete the file before appending
try:
    os.remove('barrapunto.html')
except OSError:
    pass

# Load parser and driver
BarrapuntoParser = make_parser()
BarrapuntoHandler = CounterHandler()
BarrapuntoParser.setContentHandler(BarrapuntoHandler)

# Ready, set, go!
xmlFile = request.urlopen('http://barrapunto.com/index.rss')
BarrapuntoParser.parse(xmlFile)

print("Parse complete")
