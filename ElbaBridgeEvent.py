# Copyright (c) 2015 Matteo Paoli
#FerryBoat 

#ToDo check ad add again the location value! And description! Check if null

'''
Example of google calendar event:

{
   "kind": "calendar#event",
   "etag": "\"2864972254172000\"",
   "id": "rjcrdbqfal5vmbf4i80bm6pm7g",
   "status": "confirmed",
   "htmlLink": "https://www.google.com/calendar/event?eid=cmpjcmRicWZhbDV2bWJmNGk4MGJtNnBtN2dfMjAxNTA1MzBUMTEwMDAwWiBldmQxaWZxZ2RiZ3JkdnZoaGV0NXNuYjlyb0Bn",
   "created": "2015-05-23T13:19:44.000Z",
   "updated": "2015-05-24T16:48:47.086Z",
   "summary": "toremar bisettimanale located",
   "description": "Ecco altri Dati",
   "location": "Piombino LI, Italy",
   "creator": {
    "email": "mttpla@gmail.com",
    "displayName": "Matteo Paoli"
   },
   "organizer": {
    "email": "evd1ifqgdbgrdvvhhet5snb9ro@group.calendar.google.com",
    "displayName": "elba-bridge",
    "self": true
   },
   "start": {
    "dateTime": "2015-05-30T13:00:00+02:00",
    "timeZone": "Europe/Rome"
   },
   "end": {
    "dateTime": "2015-05-30T14:00:00+02:00",
    "timeZone": "Europe/Rome"
   },
   "recurrence": [
    "RRULE:FREQ=WEEKLY;UNTIL=20161126T120000Z;INTERVAL=2;BYDAY=SA"
   ],
   "transparency": "transparent",
   "iCalUID": "rjcrdbqfal5vmbf4i80bm6pm7g@google.com",
   "sequence": 1
  }

'''
import time
from datetime import datetime


class ElbaBridgeEvent():
	timeFormat = "%Y-%m-%dT%H:%M:%S"

	def __init__(self,calId,summary,startTime,endTime, description = None, location = None):
	    self.calId = calId
	    self.summary = summary
	    self.description = description
	    self.startTime = startTime
	    self.endTime = endTime
	    self.location = location
	    self.unixtime = time.mktime(datetime.strptime(startTime[:-6],self.timeFormat).timetuple())
	    self.onlyPedestrians = False
	    if(len(summary.split(" ")) > 1):
	        summarySplitted = summary.split(" ")
	        self.company = summarySplitted[0]
	        if(summarySplitted[-1].lower() == "hydrofoil" or summarySplitted[-1].lower() == "aliscafo"):
	            self.onlyPedestrians = True 
	            self.route = " ".join(summarySplitted[1:-1])
	        else:  
	            self.route = " ".join(summarySplitted[1:]) 
	        
	    else:
	        self.company = summary
	        self.route = summary
	         
	        
	
	def toDict(self):
	    info = {}
	    #info['id'] = self.calId
	    
	    info['startTime'] = self.startTime
	    info['endTime'] = self.endTime
	    info['route'] = self.route
	    info['company'] = self.company
	    info['onlyPedestrians'] = self.onlyPedestrians
	    if(self.location != None):
	        info['location'] = self.location
	    if(self.description != None):
	        info['description'] = self.description
	    return info
	
 
    
        
        

