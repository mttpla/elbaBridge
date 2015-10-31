#Utils methods
import json, datetime
import Constants
from ElbaBridgeEvent import ElbaBridgeEvent

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
    Optional harbour, pedestrian
    Optional decriptionContain
    '''
    checkDate(params, "endDate", outputDict)
    checkDate(params, "startDate", outputDict)
    
    '''TODO
    check that startDate is before than endDate. Google will do for us... but a check is required
    '''
    
    '''TODO
    Add optional value to outputDict
    '''
    
    return outputDict

def getPrefixData(data, request):
    data['msgTime'] = datetime.datetime.now().strftime(Constants.DATETIME_PATTERN)
    data['request'] = request
    
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
    
    
    
