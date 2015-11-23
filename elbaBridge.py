#!/usr/bin/python

# Copyright (c) 2015 Matteo Paoli

print "Content-type:application/json"
print "Access-Control-Allow-Origin: *\r\n\r\n"

import cgi, cgitb
import Utils, Constants,CalendarSearch
from ElbaBridgeEvent import ElbaBridgeEvent

#log, in production switch to: cgitb.enable(display=0, logdir="/path/to/logdir")
cgitb.enable()

request = Utils.parseParameterInput(cgi.FieldStorage())

if(request['result'] == 'OK'):
    #user request is ok. Run!
    eventList = []
    
    eventList = CalendarSearch.populateElbaBrigdeEventList(request['startDate'], request['endDate'])
    
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
    
   
    print Utils.getAnswerMessage(request,eventList)
    
else:
    #user requet is wrong
    print Utils.getErrorMessage(request, request['result'])


   

  

