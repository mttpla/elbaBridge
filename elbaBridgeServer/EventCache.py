# Copyright (c) 2015 Matteo Paoli
# -*- coding: utf-8 -*-
import logging, collections,sys

#use: https://docs.python.org/2/library/collections.html#collections.OrderedDict
#odict = collections.OrderedDict()
#remove the oldest: odict.pop(odict.keys()[0])

#to update the order, remove the element and add again.

eventDict = collections.OrderedDict()
size = 200  

def getEventResult(key):
    result = None
    logging.debug("Cache: start searching")
    if key in eventDict:
        result = eventDict.pop(key)
        saveEventResult(key,result)
    logging.debug("Cache: end searching")
    logging.debug("Keys: " + str(eventDict.keys()))
    return result
    
def saveEventResult(request,events):
    logging.debug("Cache size: " +str(len(eventDict)))
    logging.debug("Cache: start saving")
    eventDict[request] = events
    logging.debug("Cache: events obj sys.getsizeof: " + str(sys.getsizeof(events)))
    logging.debug("Cache: end saving")
    #check size, and remove the last if needed.
    if(len(eventDict) > size):
        eventDict.pop(eventDict.keys()[0])
