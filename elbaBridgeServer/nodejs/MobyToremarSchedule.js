//Matteo Paoli - Copyrigth 2015

var routeDict = []; 
//["FP|Portoferraio - Piombino","DP|Cavo - Piombino","FD|Portoferraio - Cavo","RP|Rio Marina - Piombino"]
//["PF|Piombino - Portoferraio","PD|Piombino - Cavo","PR|Piombino - Rio Marina"]
//["DF|Cavo - Portoferraio","PD|Piombino - Cavo","PF|Piombino - Portoferraio","PR|Piombino - Rio Marina"]
routeDict['FP'] = 'Portoferraio-Piombino'
routeDict['PF'] = 'Piombino-Portoferraio'

routeDict['RP'] = 'Rio Marina-Piombino'
routeDict['PR'] = 'Piombino-Rio Marina'

routeDict['PD'] = 'Piombino-Cavo'
routeDict['DP'] = 'Cavo-Piombino'
routeDict['FD'] = 'Portoferraio-Cavo'
routeDict['DF'] = 'Cavo-Portoferraio'



var request = require('request');

var myferries = []

var date_param = process.argv[2]
var direction_param = process.argv[3]

if (Math.random() > 0.5){
    serverUrl = 'http://www.moby.it/mds/dwr/call/plaincall/DispoDwr.getCorse'
}else{
    serverUrl = 'http://www.toremar.it/mds/dwr/call/plaincall/DispoDwr.getCorse'
}

//console.log(serverUrl)

request({url: serverUrl,
    qs: {'callCount':1, 
			'page':'/mds/web/toremar/wdisponibilita.xpd',
			'httpSessionId':null,
			'scriptSessionId':null,
			'c0-scriptName':'DispoDwr',
			'c0-methodName':'getCorseAndata',
			'c0-id':0,
			'c0-param0':'it',
			'c0-param1': direction_param,
			'c0-param2': date_param,
			'c0-param3':'dispo',
			'c0-param4':'TOREMAR',
			'batchId':2},
    method: 'POST',
}, function (error, response, body) {
    if (!error && response.statusCode == 200) {
        //console.log(body); // Show the HTML for the Modulus homepage.
        //remove first 3 lines and remove the last one.
        var lines = body.split('\n').slice(3,-2).join('\n');  
        
        eval(lines);
        
        //console.log(JSON.stringify(s0));
        //console.log(routeDict)
        for (i = 0; i < s1.length; i++){
            var myferry = {}
            myferry['id'] = s1[i]['codice_corsa'];
            myferry['company'] = s1[i]['compagnia_corsa'] ;
            myferry['date'] = s1[i]['data_partenza'] ;
            myferry['start_time'] = s1[i]['ora_partenza'];
            //"end": {
            //"dateTime": "2015-05-30T14:00:00+02:00",
            //"timeZone": "Europe/Rome"
            //},
            // s1[i]['data_partenza'] = 03-06-2016 to 2016-06-03
            yyyymmdd = s1[i]['data_partenza'].slice(6,10)+"-" + s1[i]['data_partenza'].slice(3,5)+"-" + s1[i]['data_partenza'].slice(0,2)
            myferry['start'] = {}
            myferry['start']['dateTime'] = yyyymmdd +"T"+s1[i]['ora_partenza']+":00+02:00" ;
            myferry['end_time'] =  s1[i]['ora_arrivo'] ;
            myferry['end'] = {}
            myferry['end']['dateTime'] = yyyymmdd +"T"+s1[i]['ora_arrivo']+":00+02:00" ;
            myferry['start_time'] = s1[i]['ora_partenza'] ;
            myferry['ferry_type'] = s1[i]['tipoNave'] ;
            myferry['route_code'] =  s1[i]['codice_linea'] ;
            myferry['route'] = routeDict[s1[i]['codice_linea']]
            var summary = s1[i]['compagnia_corsa'] + " " + routeDict[s1[i]['codice_linea']]
            if(s1[i]['tipoNave'] == 'A'){
                summary = summary + " aliscafo";
            }
            myferry['summary'] =  summary ;
            
            myferries.push(myferry);
        }
        
        
        console.log(JSON.stringify(myferries))
        
        
    }
});


