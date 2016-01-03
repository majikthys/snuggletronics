
var app = angular.module('mattressApp', ['ngResource']);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.controller('MattressHeaterController', ['$scope', '$resource',
    function MattressHeaterController($scope, $resource) {

    $scope.api_mattress = $resource('/api/v1/mattress', {},{'update': { method:'PUT' }});

    //valid color range for form
    $scope.temp_values = [0,1,2,3,4,5,6,7,8,9,10]

    $scope.submit_mattress = $scope.api_mattress.get();

    var mattressHeater = this;
    mattressHeater.setTemp = function() {
       $scope.submit_mattress.power_on = true
       result_mattress = $scope.api_mattress.update($scope.submit_mattress)
       $scope.submit_mattress = result_mattress
    };

    mattressHeater.turnOff = function() {
        $scope.submit_mattress.power_on = false
        result_mattress = $scope.api_mattress.update($scope.submit_mattress)
        $scope.submit_mattress = result_mattress
    };


  }]);
