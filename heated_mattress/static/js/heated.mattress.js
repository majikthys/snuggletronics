
var app = angular.module('mattressApp', ['ngResource']);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);






app.controller('MattressHeaterController', ['$scope', '$resource',
    function MattressHeaterController($scope, $resource) {

   $scope.api_mattress = $resource('/api/mattress', {},{'update': { method:'PUT' }});
//
    raw_mattress = $scope.raw_mattress;
    raw_mattress = {
        "mattress": {
            "left_foot_power": 3,
            "left_head_power": 9,
            "left_middle_power": 2,
            "right_foot_power": 8,
            "right_head_power": 4,
            "right_middle_power": 1
        }
    };




    off_mattress = {
    "mattress": {
        "left_foot_power": 0,
        "left_head_power": 0,
        "left_middle_power": 0,
        "right_foot_power": 0,
        "right_head_power": 0,
        "right_middle_power": 0
    }
    };

    //valid color range for form
    $scope.temp_values = [0,1,2,3,4,5,6,7,8,9,10]

    $scope.mattress = $scope.api_mattress.get();
    $scope.submit_mattress = $scope.api_mattress.get();

    var mattressHeater = this;
    mattressHeater.setTemp = function() {
       $scope.mattress =  $scope.submit_mattress;
//       alert("submit:\n" + JSON.stringify($scope.mattress) );
       $scope.api_mattress.update($scope.mattress)
    };

    mattressHeater.turnOff = function() {
        $scope.mattress = off_mattress.mattress;
        $scope.submit_mattress = off_mattress.mattress;
//        alert("submit:\n" + JSON.stringify($scope.mattress) );
        $scope.api_mattress.update(off_mattress.mattress)
    };


  }]);
