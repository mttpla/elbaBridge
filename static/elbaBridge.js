// Copyright (c) 2015 Matteo Paoli

var app = angular.module('elbaBridge', ['pascalprecht.translate','ngMaterial']);


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
    'results found': 'results found'
  });
 
  $translateProvider.translations('it', {
    'From': 'Giorno di partenza',
    'To': 'A',
    'Route': 'Tratta',
    'Search': 'Trova!',
    'Loading...': 'Ricerca...',
    'Company': "Compagnia di navigazione",
    'Departure time': 'Orario di partenza',
    'Arrival time': 'Orario di arrivo',
    'Time': "Orario",
    'Only pedestrians': 'Solo passeggeri, no auto',
    'results found': 'risultati trovati'
  });
 
  $translateProvider.preferredLanguage(
      (window.navigator.userLanguage || window.navigator.language).substring(0, 2));
  $translateProvider.useSanitizeValueStrategy('escape');      
}]);

app.controller('elbaBridgeCtrl', function($scope, $http, $filter) {
    
    $scope.startDate = new Date() 
    $scope.startTime = $scope.startDate.getHours();
    $scope.noResult = true
    
    
    $scope.routes = ['--','Piombino-Portoferraio','Portoferraio-Piombino','Piombino-Rio Marina'
                     ,'Rio Marina-Piombino','Piombino-Cavo','Cavo-Piombino','Portoferraio-Cavo','Cavo-Portoferraio']
    $scope.route = '--'
    $scope.routeselected = function (routeSelected) {
        $scope.route = routeSelected;
    }
    
    $scope.companies = ['--','BluNavy','ElbaFerries','Moby','Toremar']
    $scope.company = '--'
    $scope.companyselected = function (companySelected) {
        $scope.company = companySelected;
    }

    $scope.onlyPedestrian = false;

    $scope.search = function() {
        //clean previosu data Search
        $scope.ebData = []
        //loading message
        $scope.message = $filter('translate')('Loading...')
        $scope.noResult = true;
        
        //add one hour at startDate, otherwise give me the running event.
        //ebStartDate = $filter('date')(new Date($scope.startDate.getTime()+60*60*1000), 'yyyyMMddHHmmss')
        ebStartTime = ("0" + $scope.startTime).slice(-2) + "0000";
        ebStartDate = $filter('date')($scope.startDate, 'yyyyMMdd')+ ebStartTime
        endDate = new Date($scope.startDate.getTime() + 60 * 60 * 24 * 1000); //one days more
        ebEndDate = $filter('date')(endDate, 'yyyyMMdd') + ebStartTime
        
        fullUrl = 'http://umkk91e9b477.mttpla.koding.io/elbaBridge/elbaBridge.py?startDate='+ebStartDate+'&endDate='+ebEndDate;
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
                if(parseInt(response.data.answer.length) > 0 ){
                    $scope.noResult  = false;    
                }
                
                $scope.message = response.data.status +"! " + response.data.answer.length +" "
                                 +  $filter('translate')('results found');
                $scope.debugMessage = fullUrl;
                
                $scope.ebData = response.data
            }, function errorCallback(response) {
                $scope.message = "Error! Requested url: " + fullUrl;
            });
        };
        
    $scope.search();
    
});