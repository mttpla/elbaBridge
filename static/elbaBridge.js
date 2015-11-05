// mttpla, nov 2015

var app = angular.module('elbaBridge', ['ui.bootstrap']);

app.controller('elbaBridgeCtrl', function($scope, $http, $filter) {
    
    $scope.startDate = new Date() 
    $scope.endDate = new Date(new Date().getTime() + 60 * 60 * 24 * 1000);
    $scope.routes = ['Tutte','Piombino-Portoferraio','Portoferraio-Piombino','Piombino-Rio Marina'
                     ,'Rio Marina-Piombino','Piombino-Cavo','Cavo-Piombino','Portoferraio-Cavo','Cavo-Portoferraio']
    $scope.route = 'Tutte'

    $scope.routeselected = function (routeSelected) {
        $scope.route = routeSelected
    }

    $scope.search = function() {
        ebStartDate = $filter('date')($scope.startDate, 'yyyyMMddHHmmss')
        ebEndDate = $filter('date')($scope.endDate, 'yyyyMMddHHmmss')
        
        fullUrl = 'http://umkk91e9b477.mttpla.koding.io/elbaBridge/elbaBridge.py?startDate='+ebStartDate+'&endDate='+ebEndDate;
        if($scope.route !== 'Tutte'){
            fullUrl += '&route='+$scope.route;
        }
        
        
        
        $http({method: 'GET',
            url: fullUrl
            }).then(function successCallback(response) {
                $scope.message = response.data.status +" " + response.data.answer.length ;
                $scope.ebData = response.data
            }, function errorCallback(response) {
                $scope.message = "Error!";
            });
        };

    
});