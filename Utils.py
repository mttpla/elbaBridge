# Copyright (c) 2015 Matteo Paoli

#Utils methods
import json, datetime, time
import Constants
from ElbaBridgeEvent import ElbaBridgeEvent


def checkRoute(params ,outputDict):
    outputDict['route'] =  params.getfirst('route', None)
    
def checkCompany(params ,outputDict):
    outputDict['company'] =  params.getfirst('company', None)
    
def checkOnlyPedestrians(params ,outputDict):
    outputDict['onlyPedestrians'] =  params.getfirst('onlyPedestrians', None)    

def checkDate(params, dateString ,outputDict):
     
    currentDate = params.getfirst(dateString, None)
    outputDict[dateString] = currentDate
    if(currentDate != None):
        try:
            datetime.datetime.strptime(currentDate, Constants.DATETIME_PATTERN)
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
    data['msgTime'] = datetime.datetime.now().strftime(Constants.DATETIME_PATTERN)
    data['request'] = request
    data['copyright'] = "Copyright 2015 Matteo Paoli"
    
def getErrorMessage(request, errorText = None):
    data = {}
    getPrefixData(data, request)
    data['status'] = "error"
    if(errorText != None):
        data['errorText'] = str(errorText)   
    return json.dumps(data)

    
def getAnswerMessage(request,ferryList, processUnixTime):
    data = {}
    data['status'] = "ok"
    getPrefixData(data, request)
    processUnixTime.append([time.time(),"end"])
    data['processTime'] = processUnixTime
    ferries = []
    for ferry in ferryList:
        ferries.append(ferry.toDict())
    
    data['answer'] = ferries
    return json.dumps(data)
    
    
    
