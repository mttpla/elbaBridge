var app = angular.module('elbaBridge', []);

app.controller('elbaBridgeCtrl', function($scope, $http, $filter) {
    

    $scope.search = function() {
        ebStartDate = $filter('date')($scope.startDate, 'yyyyMMddHHmmss')
        ebEndDate = $filter('date')($scope.endDate, 'yyyyMMddHHmmss')
        
        $http({method: 'GET',
            url: 'http://umkk91e9b477.mttpla.koding.io/elbaBridge/elbaBridge.py?startDate='
            +ebStartDate+'&endDate='+ebEndDate
            }).then(function successCallback(response) {
                $scope.message = response.data.status +" " + response.data.request.result ;
                $scope.ebData = response.data
            }, function errorCallback(response) {
                $scope.message = "Error!";
            });
        };

    
});