#!/usr/bin/env python
# Copyright 2015 Matteo Paoli - mttpla@gmail.com
# -*- coding: utf-8 -*-

import sys,logging,logging.config,time,os
import Utils, Constants,CalendarSearch
from ElbaBridgeEvent import ElbaBridgeEvent
from datetime import datetime

import web

urls = (
    '/elbaBridge', 'elbaBridge',
    '/', 'index'
)

class index:
    def GET(self):
        web.header('Content-Type','text/html; charset=utf-8') 
        return "ElbaBridgeServer page - Copyright 2015 Matteo Paoli"
        
class elbaBridge:
    def GET(self):
        logging.info("Request elbaBridge")
       
        
        web.header('Content-Type','application/json; charset=utf-8') 
        
        page = ""
        
        request = Utils.parseParameterInput(web.input())
        
        if(request['result'] == 'OK'):
            #user request is ok. Run!
            eventList = []
         
            eventList = CalendarSearch.populateElbaBrigdeEventList(request['startDate'], request['endDate'])
           
            startRequestUnixTime = time.mktime(datetime.strptime(request['startDate'],"%Y%m%d%H%M%S").timetuple())
            #clean startDate > of event startDate
            for event in eventList[:] :
                if(event.unixtime < startRequestUnixTime):
                    eventList.remove(event)
                else:
                    break #all other event are OK.
    
    
            #clean the event list
            
            for event in eventList[:] :
                if(request['route'] != None):
                    if( event.route.lower() != request['route'].lower()):
                        eventList.remove(event)
                        break
                if(request['company'] != None):
                    if( event.company.lower() != request['company'].lower()):
                        eventList.remove(event)
                        break
                if(request['onlyPedestrians'] == None ):
                    if (event.onlyPedestrians == True):
                        eventList.remove(event)
                        break
            page += Utils.getAnswerMessage(request,eventList)
    
        else:
            #user requet is wrong
            page += Utils.getErrorMessage(request, request['result'])
        logging.info("Served elbaBridge")    
        return page

if __name__ == "__main__":
    logging.config.fileConfig('./ElbaBridgeServer.cfg')
    logging.info("Start ElbaBridgeServer!")
    
    app = web.application(urls, globals())
    app.run()


    
   