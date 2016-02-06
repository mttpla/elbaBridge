# Copyright (c) 2015 Matteo Paoli
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser

class TraghettiLinesHtmlParser(HTMLParser):
    
    companyMap = {"//cdn.traghettilines.it/images/loghi_compagnie_result/14.gif?v=2":"Toremar",
                  "//cdn.traghettilines.it/images/loghi_compagnie_result/4.gif?v=2": "Moby",
                  "//cdn.traghettilines.it/images/loghi_compagnie_result/27.gif?v=2": "BluNavy",
                  "//cdn.traghettilines.it/images/loghi_compagnie_result/58.gif?v=2": "ElbaFerries",
                  }
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.lines = [] 
        self.line = {} 
        self.param = ""
    
    def getResults(self):
        return self.lines
    
    def handle_starttag(self, tag, attrs):
        if(tag == 'tr' ):
            if(len(attrs) == 1):
                attr = attrs[0]
                if(attr[0] == "class" and attr[1] == "a"):
                    #create new empty line
                    self.line.clear()
        if(tag == 'td' ):
            if(len(attrs) == 1):
                attr = attrs[0]
                if(attr[0] == "class"):
                    if(attr[1] == "hidden-xs"):
                        self.param = 'time'
                    if(attr[1] == "c l" ):
                        self.param = 'route'
        if(tag == 'img' ):
            if(len(attrs) == 3):
                attr = attrs[1] #second
                if(attr[0] == "src"):
                    if("loghi_compagnie_result" in attr[1]):
                        self.line['company'] = self.companyMap[attr[1]]
                    if("no_auto" in attr[1]):
                        self.line['onlyPedestrian'] = True
                        
            
    
    def handle_endtag(self, tag):
        if(tag == 'tr' and len(self.line) !=0 ):
            storeLine = self.line.copy()
            #save current line
            self.lines.append(storeLine)
            self.line.clear()
        if(tag == 'td'):
            self.param = ""
            
    def handle_data(self, data):
        if(len(self.param) != 0):
            #keep Cavo - Rio Marina to Cavo-Rio Marina
            self.line[self.param] = data.strip(' \t\n\r').replace(" - ", "-")
    
    