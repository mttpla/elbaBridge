#!/usr/bin/env python
# Copyright 2015 Matteo Paoli - mttpla@gmail.com
# -*- coding: utf-8 -*-

## installation
# apt-get python, nodejs, python-googleapi
# remenber to add manually the key.py file.

import sys,logging,logging.config,time,os,web
from datetime import datetime, date

import Utils, Constants, EventList


urls = (
    '/elbaBridge', 'elbaBridge',
    '/', 'index'
)

class index:
    def GET(self):
        logging.info("Request index page")
        web.header('Content-Type','text/html; charset=utf-8') 
        page = "<h1>ElbaBridgeServer</h1>"
        page = page + "<div>" + str(web.ctx.env) + "</div>"
        page += "<div>Copyright 2015 Matteo Paoli</div>"
        logging.info("Served index page")
        return page
        
class elbaBridge:
    def GET(self):
        logging.info("Request elbaBridge page")
        #logging.info("variables: " + str(web.ctx.env))
        #logging.info("variables REF: " + str(web.ctx.env.get('HTTP_REFERER', 'http://google.com')))
        web.header('Content-Type','application/json; charset=utf-8') 
        
        page = ""
        
        request = Utils.parseParameterInput(web.input())
        
        if(request['result'] == 'OK'):
            #user request is ok. Run!
            logging.debug("Request date: " + str(request['startDate']))
            #date requested ggmmyyyy
            d = request['startDate']
            EventList.updateEvent(Utils.getRequestDay(web.input()))
            eventList = []
            eventList.extend(EventList.events)
            #All in UTC
            unixTime = time.mktime(datetime.utcnow().timetuple()) 
            logging.debug("Current unix time: " + str(unixTime))
            
            startRequestUnixTime = time.mktime(datetime.strptime(request['startDate'],"%Y%m%d%H%M%S").timetuple())
            endRequestUnixTime = time.mktime(datetime.strptime(request['endDate'],"%Y%m%d%H%M%S").timetuple())
            #clean the event list
            
            for event in eventList[:] :
                if(event.unixtime < startRequestUnixTime):
                    #logging.debug("remove Event: " + str(event.route) + " -- " + str(event.startTime))
                    eventList.remove(event)
                    continue
                if(event.unixtime > endRequestUnixTime):
                    #logging.debug("remove Event: " + str(event.route) + " -- " + str(event.startTime))
                    del eventList[eventList.index(event):]
                    break
                if(request['route'] != None):
                    if( event.route.lower() != request['route'].lower()):
                        eventList.remove(event)
                        continue
                if(request['company'] != None):
                    if( event.company.lower() != request['company'].lower()):
                        eventList.remove(event)
                        continue
                if(request['onlyPedestrians'] == None ):
                    if (event.onlyPedestrians == True):
                        eventList.remove(event)
                        continue
            page += Utils.getAnswerMessage(request,eventList)
    
        else:
            #user requet is wrong
            page += Utils.getErrorMessage(request, request['result'])
        logging.info("Served elbaBridge page")    
        return page

if __name__ == "__main__":
    logging.config.fileConfig(os.path.dirname(os.path.realpath(__file__)) + '/ElbaBridgeServer.cfg')
    logging.info("Start ElbaBridgeServer!")
    EventList.populate()
    #EventList.importEventRange(date(2016, 7, 1), date(2016, 8, 31))
    
    logging.info("EventList populated, event numbers: " + str(len(EventList.events)))
    
    app = web.application(urls, globals())
    app.run()
    


    
   