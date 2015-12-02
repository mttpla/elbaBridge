# Copyright (c) 2015 Matteo Paoli

#quering to google Calendar
import urllib2, sys, json, time, logging
from datetime import datetime
import Key
from ElbaBridgeEvent import ElbaBridgeEvent
import EventCache

def buildUrl(min, max, eventID = None):
	#2015-05-05T12%3A00%3A00%2B02%3A00 - 12:00:00+02:00
	google_url = "https://www.googleapis.com/calendar/v3/calendars/"+Key.calID+"/events"
	if(eventID != None):
	    google_url += "/"+eventID+"/instances"
	google_url += "?key="+Key.key
	if(eventID != None):
	    google_url += "&fields=items"
	google_url += "&timeMin="+min+"&timeMax="+max+"&maxResults=100&sigleEvents=true"
	return google_url
	

def getGoogleDate(datetime):
    #starting pattern "%Y%m%d%H%M%S"
    #required end pattern T00%3A00%3A00%2B01%3A00
    #timezone GMT +1 ... or +2 question of Daylight savings time
    if(len(datetime) == 14):
        #2015-10-10T10:00:00+02:00
        date = datetime[0:4]+"-"+datetime[4:6]+"-"+datetime[6:8]
        time = "T"+datetime[8:10]+"%3A"+datetime[10:12]+"%3A"+datetime[12:14]+"%2B01%3A00"
        return date+time
    return None
    
def createEvent(myItem):
    event = ElbaBridgeEvent(myItem["id"],myItem["summary"],
                              myItem["start"]["dateTime"],myItem["end"]["dateTime"])
    if('description' in myItem):
            event.description = myItem['description']
    if('location' in myItem):
            event.location = myItem['location'] 
    return event

def populateElbaBrigdeEventList(startDate, endDate):
    min = getGoogleDate(startDate)
    max = getGoogleDate(endDate)
    
    logging.debug("EventCache request: " + str(startDate)+str(endDate))
    logging.debug("Cache: EventCache obj sys.getsizeof: " + str(sys.getsizeof(EventCache)))
    events = EventCache.getEventResult(str(startDate)+str(endDate))
    if(events == None):
        events = []
        logging.debug("No result in EventCache")
        data = json.load(urllib2.urlopen(buildUrl(min,max)))
        logging.debug("Creting Event")
        for item in data["items"]:
            if "recurrence" in item:
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
        if(len(events)>0):
            logging.debug("Save Event, #: " + str(len(events)))
            EventCache.saveEventResult(str(startDate)+str(endDate),events)
    logging.debug("Event List done")
    return events
    
   

