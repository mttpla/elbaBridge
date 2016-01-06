# Copyright (c) 2015 Matteo Paoli
# -*- coding: utf-8 -*-

import logging, json, urllib2
import Utils, Constants, Key
from Event import Event


events = []
requestedDate = []


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


def updateEvent(eventDate):
    #serach event using reqPost.js external software
    #check if event is in eventList, needed to add a unique field: es: summary+statdate
    #http://stackoverflow.com/questions/9371114/check-if-list-of-objects-contain-an-object-with-a-certain-attribute-value
    logging.debug("Date requested: " + str(eventDate))
    if not eventDate in requestedDate:
        destinations = ['FP', 'PF']
        for dest in destinations:
            command = "nodejs MobyToremarSchedule.js " + str(eventDate) + " " + str(dest) 
            result = Utils.runCommand(command , "./nodejs")
            #logging.debug(result)
            if result['returncode'] == 0 :
                #logging.debug(result['stdout'])
                newEvents = json.loads(result['stdout'][:-1])
                #logging.debug(newEvents)
                global events
                for newEvent in newEvents:
                    #logging.debug("Event: " + str(event))
                    newEventID = str(newEvent['start']['dateTime'][:-6]+newEvent['summary']).lower()
                    if any(ev.identifier.lower() == newEventID.lower() for ev in events) :
                        logging.debug("Event duplicated: " + str(newEventID))
                    else:
                        logging.debug("Event added: " + str(newEventID))
                        events.append(createEvent(newEvent))
            else:
                logging.error("Node reqPost.js command got a error! Command:  " +str(command) + " -- " + str(result['sterr']))
        requestedDate.append(eventDate)
        events = sorted(events, key= lambda ElbaBridgeEvent: ElbaBridgeEvent.unixtime)
    else:
        logging.debug("No updated required, event in cache.")
	
	
def populate():
    min = "2016-01-07T12%3A00%3A00%2B02%3A00"
    max = "2016-12-31T12%3A00%3A00%2B02%3A00"
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
    
    