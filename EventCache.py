# Copyright (c) 2015 Matteo Paoli
# -*- coding: utf-8 -*-
import logging, collections

#use: https://docs.python.org/2/library/collections.html#collections.OrderedDict
#odict = collections.OrderedDict()
#remove the oldest: odict.pop(odict.keys()[0])

#to update the order, remove the element and add again.

eventDict = collections.OrderedDict()
size = 5

def getEventResult(key):
    result = None
    logging.debug("Cache: start searching")
    if key in eventDict:
        result = eventDict[key]
    logging.debug("Cache: end searching")
    return result
    
def saveEventResult(request,events):
    logging.debug("Cache size: " +str(len(eventDict)))
    logging.debug("Cache: start savinging")
    #check size, and remove the last if needed. 
    eventDict[request] = events
    logging.debug("Cache: end savinging")
