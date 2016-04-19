#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import os.path

class myContentHandler(ContentHandler):

    # Guarda en un fichero html la lista de los titulares de las noticias
    # donde cada titulo es un link a su respectiva noticia
    # USAGE: ./xml-parser-barrapunto.py barrapunto.rss
    if os.path.exists("bp.html"):
        fichHTML = open("bp.html", "w")
    else:
        fichHTML = open("bp.html", "a")
    title = ""
    link = ""

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                # To avoid Unicode trouble
                self.title = self.theContent.encode('utf-8')
                print self.title
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = self.theContent.encode('utf-8')
                print self.link
                newline = '<li><a href="'+ self.link + '">' + self.title + '</a></li>' + '\n'
                self.fichHTML.write(newline)
                self.inContent = False
                self.theContent = ""


    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


# --- Main prog

if len(sys.argv)<2:
    print "Usage: python xml-parser-barrapunto.py <document>"
    print
    print " <document>: file name of the document to parse"
    sys.exit(1)

# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = open(sys.argv[1],"r")
theParser.parse(xmlFile)

print "Parse complete"
