# Copyright (c) 2015 Matteo Paoli
# -*- coding: utf-8 -*-

import logging, json, urllib2
import Utils, Constants, Key
from Event import Event


events = []


def createEvent(myItem):
    event = Event(myItem["id"],myItem["summary"],myItem["start"]["dateTime"],myItem["end"]["dateTime"])
    if('description' in myItem):
            event.description = myItem['description']
    if('location' in myItem):
            event.location = myItem['location'] 
    return event

def buildUrl(min = None, max = None, eventID = None):
	#2015-05-05T12%3A00%3A00%2B02%3A00 - 12:00:00+02:00
	google_url = "https://www.googleapis.com/calendar/v3/calendars/"+Key.calID+"/events"
	if(eventID != None):
	    google_url += "/"+eventID+"/instances"
	google_url += "?key="+Key.key
	if(eventID != None):
	    google_url += "&fields=items"
	if(min != None):
	    google_url += "&timeMin="+min
	if(max != None):
	    google_url += "&timeMax="+max
	return google_url
	
def populate():
    min = "2015-05-05T12%3A00%3A00%2B02%3A00"
    max = "2019-05-05T12%3A00%3A00%2B02%3A00"
    global events
    data = json.load(urllib2.urlopen(buildUrl(min,max)))
    logging.debug("Creating Event")
    for item in data["items"]:
        if "recurrence" in item:
            #logging.debug("Recurrence, event url: " + str(buildUrl(min,max,item["id"])))
            subData = json.load(urllib2.urlopen(buildUrl(min,max,item["id"])))
            for subItem in subData["items"]:
                if('summary' in subItem):
                    events.append(createEvent(subItem))
        else:
            if('summary' in item):
                events.append(createEvent(item))
    
    logging.debug("Event list created")
    
    events = sorted(events, key= lambda ElbaBridgeEvent: ElbaBridgeEvent.unixtime)
    logging.debug("Event List sorted")
    
    