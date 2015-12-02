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
    'From': 'From',
    'To': 'To',
    'Route': 'Route',
    'Search': 'Search!',
    'Loading...': 'Loading...',
    'Company': 'Company',
    'Departure time': 'Departure time',
    'Arrival time': 'Arrival time',
    'Time': 'Time',
    'Only pedestrians': 'Only Pedestrions',
    'results found': 'results found',
    'disclaimer' : 'All trademarks or logos show in this web site are of their owner.',
    'disclaimer2' : "The infos, time schedules and prices can change wihtout any notice. Please, check on the offical web site.",
    'Departure day' : 'Departure day',
    'descriptionText' : 'Ferryboat time schedule to and from Elba Island',
    'Sorry, no result': 'No result available, try to change your filter on the left tab.',
    'BUTTON_LANG_EN': 'english',
    'BUTTON_LANG_IT': 'italian'
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
    'BUTTON_LANG_EN': 'english',
    'BUTTON_LANG_IT': 'italian'
  });
 
  $translateProvider.preferredLanguage(
      (window.navigator.userLanguage || window.navigator.language).substring(0, 2));

  $translateProvider.useSanitizeValueStrategy('escape');      
}]);

app.controller('elbaBridgeCtrl', function($scope, $http, $filter, $translate) {
    
    $scope.startDate = new Date() 
    $scope.startTime = $scope.startDate.getHours();
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
                       
        };
    

    $scope.search = function() {
        //clean previosu data Search
        $scope.ebData = []
        //loading message
        $scope.loadingResult = true
     
        
        //add one hour at startDate, otherwise give me the running event.
        //ebStartDate = $filter('date')(new Date($scope.startDate.getTime()+60*60*1000), 'yyyyMMddHHmmss')
        ebStartTime = ("0" + $scope.startTime).slice(-2) + "0000";
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