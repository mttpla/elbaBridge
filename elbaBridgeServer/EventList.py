# Copyright (c) 2015 Matteo Paoli
# -*- coding: utf-8 -*-

import logging, json, urllib2, time, urllib, hashlib
from datetime import date, timedelta as td
from TraghettiLinesHtmlParser import TraghettiLinesHtmlParser
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

def importEventRange(startdate, enddate):
    delta = enddate - startdate
    for i in range(delta.days + 1):
        updateEvent((startdate + td(days=i)))
        #time.sleep(1)

def updateEventOnMobyToremar(eventDate):
    destinations = ['FP', 'PF']
    for dest in destinations:
        #search event using reqPost.js external software
        command = "nodejs MobyToremarSchedule.js " + str(eventDate) + " " + str(dest) 
        result = Utils.runCommand(command , "./nodejs")
        #logging.debug(result)
        if result['returncode'] == 0 :
            #logging.debug(result['stdout'])
            newEvents = json.loads(result['stdout'][:-1])
            #logging.debug(newEvents)
            global events
            
            #check if event is in eventList, needed to add a unique field: es: summary+statdate
            #http://stackoverflow.com/questions/9371114/check-if-list-of-objects-contain-an-object-with-a-certain-attribute-value
    
            for newEvent in newEvents:
                #logging.debug("Event: " + str(event))
                newEventID = str(newEvent['start']['dateTime'][:-6]+newEvent['summary']).lower()
                if any(ev.identifier.lower() == newEventID.lower() for ev in events) :
                    #logging.debug("Event duplicated: " + str(newEventID))
                    pass
                else:
                    #logging.debug("Event added: " + str(newEventID))
                    events.append(createEvent(newEvent))
            requestedDate.append(eventDate)
            events = sorted(events, key= lambda ElbaBridgeEvent: ElbaBridgeEvent.unixtime)
        else:
            logging.error("Nodejs command got a error! Command:  " +str(command) + " -- " + str(result['sterr']))

def updateEventOnTraghettiLines(eventDate):
    #http://www.traghettilines.it/results.aspx?Pdestinazione=3&Pdata=22/08/2016
    html = ""
    try:
        html = urllib2.urlopen("http://www.traghettilines.it/results.aspx?Pdestinazione=3&Pdata="+eventDate.strftime("%d/%m/%Y")).read()
    
        if(len(html) > 100):
            htmlParser = TraghettiLinesHtmlParser()
            htmlParser.feed(html)
            global events
            for eventLine in htmlParser.getResults():
                #logging.debug(eventLine)
                newEvent = {}
                newEvent['id'] = "traghettilines"+hashlib.md5(str(eventLine)).hexdigest()
                newEvent['summary'] = eventLine['company'] + " " + eventLine['route']
                if('onlyPedestrian' in eventLine):
                    newEvent['summary'] = newEvent['summary'] + " aliscafo"
                #"dateTime": "2015-05-30T14:00:00+02:00"
                day = eventDate.strftime("%Y-%m-%d")
                eventLineTimeSplitted = eventLine['time'].split("-")
                newEvent['start'] = {}
                newEvent['end'] = {}
                newEvent["start"]["dateTime"] = day +"T"+eventLineTimeSplitted[0].replace(".",":")+":00+02:00"
                newEvent["end"]["dateTime"] = day +"T"+eventLineTimeSplitted[1].replace(".",":")+":00+02:00"
                #logging.debug("time: " +str(eventLine['time']) + " --> " + str(newEvent["start"]["dateTime"]))
                newEventID = str(newEvent['start']['dateTime'][:-6]+newEvent['summary']).lower()
                if any(ev.identifier.lower() == newEventID.lower() for ev in events) :
                    #logging.debug("Event duplicated: " + str(newEventID))
                    pass
                else:
                    logging.debug("Event added: " + str(newEventID))
                    events.append(createEvent(newEvent))
            requestedDate.append(eventDate)
            events = sorted(events, key= lambda ElbaBridgeEvent: ElbaBridgeEvent.unixtime)
    except:
        logging.error("failed to get data from traghettilines")

def updateEvent(eventDate):
    logging.debug("Date requested: " + str(eventDate.strftime("%d/%m/%Y")))
    if not eventDate in requestedDate:
        # updateEventOnMobyToremar(eventDate.strftime("%d%m%Y")) to check and test
        updateEventOnTraghettiLines(eventDate)
    else:
        logging.debug("No updated required, event in cache.")

def pushToCalender(event):
    #TODO, add the ability to push new events to googleCalendar
    logging.debug("push to google calendar")
    
    
	
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
    
    