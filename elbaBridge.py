#!/usr/bin/python

# Copyright (c) 2015 Matteo Paoli

print "Content-type:application/json"
print "Access-Control-Allow-Origin: *\r\n\r\n"

import cgi, cgitb, time
import Utils, Constants,CalendarSearch
from ElbaBridgeEvent import ElbaBridgeEvent
from datetime import datetime

processUnixTime = []
processUnixTime.append([time.time(),"start"])
#log, in production switch to: cgitb.enable(display=0, logdir="/path/to/logdir")
cgitb.enable()

request = Utils.parseParameterInput(cgi.FieldStorage())

            

if(request['result'] == 'OK'):
    #user request is ok. Run!
    eventList = []
    startRequestUnixTime = time.mktime(datetime.strptime(request['startDate'],"%Y%m%d%H%M%S").timetuple())
    
    processUnixTime.append([time.time(),"startHttpRequest"])
    eventList = CalendarSearch.populateElbaBrigdeEventList(request['startDate'], request['endDate'])
    processUnixTime.append([time.time(),"endHttpRequest"])
    
    #clean startDate > of event startDate
    for event in eventList[:] :
        if(event.unixtime < startRequestUnixTime):
            eventList.remove(event)
        else:
            break #all other event are OK.
    
    
    #clean the event list
    if(request['route'] != None):
        for event in eventList[:] :
            if( event.route.lower() != request['route'].lower()):
                eventList.remove(event)
    
    
    if(request['company'] != None):
        for event in eventList[:] :
            if( event.company.lower() != request['company'].lower()):
                eventList.remove(event)   
    
    
    if(request['onlyPedestrians'] == None ):
        for event in eventList[:]:
            if (event.onlyPedestrians == True):
                eventList.remove(event) 
    
    
   
    print Utils.getAnswerMessage(request,eventList,processUnixTime)
    
else:
    #user requet is wrong
    print Utils.getErrorMessage(request, request['result'])


   

  

