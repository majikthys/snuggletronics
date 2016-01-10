var heatedMattressControllers = angular.module('heatedMattressControllers', []);


//heatedMattressControllers.controller('MattressHeaterController', ['$scope', '$http', '$resource',
//  function ($scope, $http) {
//  alert("this is happening")
////    $http.get('phones/phones.json').success(function(data) {
////      $scope.phones = data;
////    });
//
//    $scope.orderProp = 'age';
//  }]);
//
//heatedMattressControllers.controller('PhoneDetailCtrl', ['$scope', '$routeParams',
//  function($scope, $routeParams) {
//    $scope.phoneId = $routeParams.phoneId;
//        $scope.orderProp = 'age';
//
//  }]);
//
heatedMattressControllers.filter('digits', function() {
    return function(input) {
       if (input < 10) input = '0' + input;

      return input;
    }
  });

heatedMattressControllers.controller('MattressHeaterController', ['$scope', '$resource',
    function MattressHeaterController($scope, $resource) {

    var Mattress = $resource('/api/v1/mattress', {},{'update': { method:'PUT' }});
    var MattressJobs = $resource('/api/v1/mattress/jobs', {}, {'get': {method: 'GET', isArray: true}});

    //valid color range for form
    $scope.temp_values = [0,1,2,3,4,5,6,7,8,9,10]
    $scope.hour_values = []
    for (var i = 0; i <= 23; i++) {
        $scope.hour_values.push(i);
    }

    $scope.minute_values = []
    for (var i = 0; i <= 59; i++) {
        $scope.minute_values.push(i);
    }

    $scope.submit_mattress = Mattress.get();
    $scope.mattress_jobs = MattressJobs.get();
    $scope.submit_job_hour=0;
    $scope.submit_job_minute=0;


    var mattressHeater = this;
    mattressHeater.setTemp = function() {
       $scope.submit_mattress.power_on = true
       result_mattress = Mattress.update($scope.submit_mattress)
       $scope.submit_mattress = result_mattress
    };

    mattressHeater.turnOff = function() {
        $scope.submit_mattress.power_on = false
        result_mattress = Mattress.update($scope.submit_mattress)
        $scope.submit_mattress = result_mattress
    };

    mattressHeater.addJob = function() {
        $scope.submit_mattress.hour = $scope.submit_job_hour
        $scope.submit_mattress.minute = $scope.submit_job_minute
        MattressJobs.save($scope.submit_mattress)
        $scope.submit_mattress = Mattress.get();
        $scope.mattress_jobs = MattressJobs.get();
    };

    mattressHeater.deleteJob = function(mattress_job) {
        MattressJobs.remove(mattress_job)
        $scope.mattress_jobs = MattressJobs.get();
     };

  }]);
