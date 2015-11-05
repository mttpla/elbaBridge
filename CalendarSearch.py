#quering to google Calendar
import urllib2, sys, json, time
from datetime import datetime
import Key
from ElbaBridgeEvent import ElbaBridgeEvent

def buildUrl(min, max, eventID = None):
	#2015-05-05T12%3A00%3A00%2B02%3A00 - 12:00:00+02:00
	google_url = "https://www.googleapis.com/calendar/v3/calendars/"+Key.calID+"/events"
	if(eventID != None):
	    google_url += "/"+eventID+"/instances"
	google_url += "?key="+Key.key
	if(eventID != None):
	    google_url += "&fields=items"
	google_url += "&timeMin="+min+"&timeMax="+max+"&maxResults=100"
	return google_url

def getGoogleDate(datetime):
    #starting pattern "%Y%m%d%H%M%S"
    #required end pattern T00%3A00%3A00%2B02%3A00
    if(len(datetime) == 14):
        #2015-10-10T10:00:00+02:00
        date = datetime[0:4]+"-"+datetime[4:6]+"-"+datetime[6:8]
        time = "T"+datetime[8:10]+"%3A"+datetime[10:12]+"%3A"+datetime[12:14]+"%2B02%3A00"
        return date+time
    return None
    
    

def populateElbaBrigdeEventList(startDate, endDate):
    
    events = []
    min = getGoogleDate(startDate)
    max = getGoogleDate(endDate)
    
    data = json.load(urllib2.urlopen(buildUrl(min,max)))
    
    for item in data["items"]:
        if "recurrence" in item:
            subData = json.load(urllib2.urlopen(buildUrl(min, max, item["id"])))
            for subItem in subData["items"]:
                events.append(ElbaBridgeEvent(subItem["id"],subItem["summary"],
                              subItem["start"]["dateTime"],subItem["end"]["dateTime"]))
                
        else:
            events.append(ElbaBridgeEvent(item["id"],item["summary"],item["start"]["dateTime"],
                          item["end"]["dateTime"]))
    
    events = sorted(events, key= lambda ElbaBridgeEvent: ElbaBridgeEvent.unixtime)
    return events
    
   
