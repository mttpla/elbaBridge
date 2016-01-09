// Copyright (c) 2015 Matteo Paoli

var app = angular.module('elbaBridge', ['pascalprecht.translate','ngMaterial'])
 .filter('addingSpaces', function() {
  return function(input) {
    return input.replace("-", " - ");
  };
})
;


app.config(['$translateProvider', function ($translateProvider) {
  $translateProvider.translations('en', {
    'From': 'Departure day',
    'To': 'To',
    'Route': 'Route',
    'Search': 'Search!',
    'Loading...': 'Loading...',
    'Company': 'Company',
    'Departure time': 'Departure time',
    'Arrival time': 'Arrival time',
    'Time': 'Time',
    'Only pedestrians': 'Only Pedestrians, no car',
    'results found': 'results found',
    'disclaimer' : 'All trademarks or logos show in this web site are of their owner.',
    'disclaimer2' : "The infos, time schedules and prices can change without any notice. Please, check on the official web site.",
    'Departure day' : 'Departure day',
    'descriptionText' : 'Ferryboat time schedule to and from Elba Island',
    'Sorry, no result': 'No result available, try to change your filter on the left tab.',
    'Duration': 'Duration',
    'Hours' : 'Hours',
    'Minutes' : 'Minutes'
  });
 
  $translateProvider.translations('it', {
    'From': 'Giorno di partenza',
    'To': 'A',
    'Route': 'Tratta',
    'Search': 'Trova!',
    'Loading...': 'Ricerca...',
    'Company': "Compagnia",
    'Departure time': 'Orario di partenza',
    'Arrival time': 'Orario di arrivo',
    'Time': "Orario",
    'Only pedestrians': 'Solo passeggeri, no auto',
    'results found': 'risultati trovati',
    'disclaimer': 'I marchi, loghi, denominazioni di aziende menzionati all’interno di questo sito restano comunque di proprietà dei rispettivi titolari.',
    'disclaimer2' : 'Inoltre i listini prezzi, orari, date o altro materiale informativo pubblicato su questo sito è suscettibile a variazioni. Siete quindi invitati a chiedere conferma alle strutture interessate.',
    'Departure day' : 'Giorno',
    'descriptionText' : 'Orario delle partenze da e per l\'Isola d\'Elba.',
    'Sorry, no result': 'Nessun risultato disponibile, si consiglia di provare a cambiare i filtri di ricerca.',
    'Duration': 'Durata',
    'Hours' : 'Ore',
    'Minutes' : 'Minuti'
  });
  
  $translateProvider.translations('de', {
    'From': 'Abfahrtstag',
    'To': 'Nach',
    'Route': 'Route',
    'Search': 'Suche',
    'Loading...': 'Bitte warten...',
    'Company': 'Schifffahrtsunternehmen',
    'Departure time': 'Abfahrt',
    'Arrival time': 'Ankunft',
    'Time': "Zeit",
    'Only pedestrians': 'Nur Passagiere, kein Auto',
    'results found': 'suchergebnisse',
    'Departure day' : 'Datum',
    'descriptionText' : 'Fahrplan Insel Elba.',
    'Sorry, no result': 'Kein Ergebnis gefunden: ändern Sie bitte Suchkriterien.',
    'Duration': 'Fahrzeit',
    'Hours' : 'Stunde',
    'Minutes' : 'Minute',
    'disclaimer' : 'All trademarks or logos show in this web site are of their owner.',
    'disclaimer2' : "The infos, time schedules and prices can change without any notice. Please, check on the official web site.",
   
  });
  
  $translateProvider.translations('fr', {
    'From': 'Jour de départ',
    'To': 'Une',
    'Route': 'Itinéraire',
    'Search': 'Chercher!',
    'Loading...': 'Chargement...',
    'Company': "Société",
    'Departure time': 'Heure de départ',
    'Arrival time': 'Heure d\'arrivée',
    'Time': "Heure",
    'Only pedestrians': 'Passagers,	no véhicul',
    'results found': 'résultats trouvés',
    'disclaimer' : 'All trademarks or logos show in this web site are of their owner.',
    'disclaimer2' : "The infos, time schedules and prices can change without any notice. Please, check on the official web site.",
    'Departure day' : 'Jour',
    'descriptionText' : 'Les heures de départ de et vers l\'Ile d\'Elbe',
    'Sorry, no result': 'Il n\'y a pas de résultats , vous pouvez essayer de changer le filtre de recherche.',
    'Duration': 'Durée',
    'Hours' : 'Hours',
    'Minutes' : 'Minutes'
  });
  
  $translateProvider.translations('es', {
    'From': 'Día de salida',
    'To': 'la',
    'Route': 'Ruta',
    'Search': 'Buscar!',
    'Loading...': 'Cargando...',
    'Company': "Compañía",
    'Departure time': 'Hora de salid',
    'Arrival time': 'Hora de llegada',
    'Time': "Tiempo",
    'Only pedestrians': 'Sólo los pasajeros , sin coche',
    'results found': 'resultados',
    'disclaimer' : 'All trademarks or logos show in this web site are of their owner.',
    'disclaimer2' : "The infos, time schedules and prices can change without any notice. Please, check on the official web site.",
    'Departure day' : 'Día',
    'descriptionText' : 'Tiempos partir hacia y desde el Isla de Elba',
    'Sorry, no result': 'No hay resultados , se puede tratar de cambiar el filtro de búsqueda.',
    'Duration': 'Duración',
    'Hours' : 'horas',
    'Minutes' : 'minutos'
  });
 
 
  $translateProvider.preferredLanguage(
      (window.navigator.userLanguage || window.navigator.language).substring(0, 2));

  $translateProvider.useSanitizeValueStrategy('escape');      
}]);

app.controller('elbaBridgeCtrl', function($scope, $http, $filter, $translate) {
    
    moment.locale('it', {
    relativeTime : {
        future: "in %s",
        past:   "%s fa",
        s:  "secondi",
        m:  "un minuto",
        mm: "%d minuti",
        h:  "un'ora",
        hh: "%d ore"
        }
    });
    
    moment.locale('fr',{
       relativeTime : {
        future : "dans %s",
        past : "il y a %s",
        s : "quelques secondes",
        m : "une minute",
        mm : "%d minutes",
        h : "une heure",
        hh : "%d heures"
    } 
    });
    
    
    moment.locale((window.navigator.userLanguage || window.navigator.language).substring(0, 2));
    $scope.startDate = new Date() 
    $scope.startHours = $scope.startDate.getHours();
    $scope.startMinutes = $scope.startDate.getMinutes();
    $scope.currentYear = $scope.startDate.getFullYear();
    
    $scope.routes = ['--','Piombino-Portoferraio','Portoferraio-Piombino','Piombino-Rio Marina'
                     ,'Rio Marina-Piombino','Piombino-Cavo','Cavo-Piombino','Portoferraio-Cavo','Cavo-Portoferraio']
    $scope.route = '--'
    $scope.routeselected = function (routeSelected) {
        $scope.route = routeSelected;
    }
    
    $scope.companyLinks = {'BluNavy':"http://www.blunavytraghetti.com/", 'ElbaFerries':"http://www.elba-ferries.it/", 
         'Moby':"http://www.moby.it", 'Toremar': "http://www.toremar.it"}
    
    $scope.companies = ['--','BluNavy','ElbaFerries','Moby','Toremar']
   
    $scope.company = '--'
    $scope.companyselected = function (companySelected) {
        $scope.company = companySelected;
    }
    
    $scope.onlyPedestrian = false;
    
    
    $scope.changeLanguage = function (key) {
          $translate.use(key);
          moment.locale(key); 
        };
      
    $scope.isNextDay = function (ferryStartTime) {
        var timeDelta = moment(ferryStartTime).diff($scope.startDate,'days')
        if(timeDelta > 0){
            return true;
        }else{
            return false;
        }
        };    
    
    $scope.duration = function (ferryStartTime, ferryEndTime) {
        return moment(ferryEndTime).from(ferryStartTime)
        };    
    
    

    $scope.search = function() {
        //clean previosu data Search
        $scope.ebData = []
        //loading message
        $scope.loadingResult = true
     
        
        //add one hour at startDate, otherwise give me the running event.
        //ebStartDate = $filter('date')(new Date($scope.startDate.getTime()+60*60*1000), 'yyyyMMddHHmmss')
        ebStartTime = ("0" + $scope.startHours).slice(-2) + ("0" + $scope.startMinutes).slice(-2) +"00";
        ebStartDate = $filter('date')($scope.startDate, 'yyyyMMdd')+ ebStartTime
        endDate = new Date($scope.startDate.getTime() + 60 * 60 * 24 * 1000); //one days more
        ebEndDate = $filter('date')(endDate, 'yyyyMMdd') + ebStartTime
        
        fullUrl = './elbaBridgeServer/elbaBridge?startDate='+ebStartDate+'&endDate='+ebEndDate;
        if($scope.route !== '--'){
            fullUrl += '&route='+$scope.route;
        }
        if($scope.company !== '--'){
            fullUrl += '&company='+$scope.company;
        }
        if($scope.onlyPedestrians){
            fullUrl += '&onlyPedestrians=true';
        }
        
        
        
        $http({method: 'GET',
            url: fullUrl
            }).then(function successCallback(response) {
                $scope.loadingResult = false
                if(parseInt(response.data.answer.length) > 0 ){
                    $scope.noResult  = false;    
                    $scope.resultLen =  response.data.answer.length               
                    //$scope.debugMessage = response.data.status +"! url: " + fullUrl  ;
                    $scope.ebData = response.data.answer
                }else{
                    $scope.resultLen = 0
                    $scope.noResult = true;
                }
            }, function errorCallback(response) {
                $scope.loadingResult = false
                $scope.resultLen = "Error! Requested url: " + fullUrl;
            });
        };
        
    $scope.search();
    
});