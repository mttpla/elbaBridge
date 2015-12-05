# Copyright (c) 2015 Matteo Paoli

#Utils methods
import json, time
from datetime import datetime
import Constants


def checkRoute(params ,outputDict):
    outputDict['route'] =  params.get('route', None)
    
def checkCompany(params ,outputDict):
    outputDict['company'] =  params.get('company', None)
    
def checkOnlyPedestrians(params ,outputDict):
    outputDict['onlyPedestrians'] =  params.get('onlyPedestrians', None)    

def checkDate(params, dateString ,outputDict):
    currentDate = params.get(dateString, None)
    outputDict[dateString] = currentDate
    if(currentDate != None):
        try:
            datetime.strptime(currentDate, Constants.URL_DATETIME_PATTERN)
        except ValueError:
            outputDict['result'] = "Error: " + dateString + ' is not a valid date. Pattern required: ' + Constants.DATETIME_PATTERN
    else:
        outputDict['result'] = "Error: " + dateString + ' missing'
        
        
def parseParameterInput(params):
    outputDict = {'result': 'OK'}
    
    '''
    Checking the GET input.
    
    Required startDate and endDate
    Optional route, pedestrian
    Optional decriptionContain
    '''
    checkDate(params, "endDate", outputDict)
    checkDate(params, "startDate", outputDict)
    
    checkRoute(params, outputDict)
    
    checkCompany(params, outputDict)
    
    checkOnlyPedestrians(params, outputDict)
    
    return outputDict

def getPrefixData(data, request):
    data['version'] = Constants.VERSION
    data['msgTime'] = datetime.now().strftime(Constants.URL_DATETIME_PATTERN)
    data['request'] = request
    data['copyright'] = "Copyright 2015 Matteo Paoli"
    
def getErrorMessage(request, errorText = None):
    data = {}
    getPrefixData(data, request)
    data['status'] = "error"
    if(errorText != None):
        data['errorText'] = str(errorText)   
    return json.dumps(data)

    
def getAnswerMessage(request,ferryList):
    data = {}
    data['status'] = "ok"
    getPrefixData(data, request)
   
    ferries = []
    for ferry in ferryList:
        ferries.append(ferry.toDict())
    
    data['answer'] = ferries
    return json.dumps(data)
    
    
    
