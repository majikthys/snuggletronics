
var app = angular.module('mattressApp', ['ngResource']);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);



// creating an 'update' method for Mattress
app.factory('Mattress', ['$resource', function($resource) {
return $resource('/api/mattress', null,
    {
        'update': { method:'PUT' }
    });
}]);

app.controller('TodoListController', function() {
    var todoList = this;
    todoList.todos = [
      {text:'learn angular', done:true},
      {text:'build an angular app', done:false}];

    todoList.addTodo = function() {
      todoList.todos.push({text:todoList.todoText, done:false});
      todoList.todoText = '';
    };

    todoList.remaining = function() {
      var count = 0;
      angular.forEach(todoList.todos, function(todo) {
        count += todo.done ? 0 : 1;
      });
      return count;
    };

    todoList.archive = function() {
      var oldTodos = todoList.todos;
      todoList.todos = [];
      angular.forEach(oldTodos, function(todo) {
        if (!todo.done) todoList.todos.push(todo);
      });
    };
  });


app.controller('MattressHeaterController', ['$scope', '$resource',
    function MattressHeaterController($scope, $resource) {

   $scope.api_mattress = $resource('/api/mattress');

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

//    $scope.mattress = raw_mattress.mattress;
//    $scope.submit_mattress = raw_mattress.mattress;

    $scope.mattress = $scope.api_mattress.get();
    $scope.submit_mattress = $scope.api_mattress.get();

    var mattressHeater = this;
    mattressHeater.setTemp = function() {
       $scope.mattress =  $scope.submit_mattress;
       alert("submit:\n" + JSON.stringify($scope.mattress) );
    };

    mattressHeater.turnOff = function() {
        $scope.mattress = off_mattress.mattress;
        $scope.submit_mattress = off_mattress.mattress;
        alert("submit:\n" + JSON.stringify($scope.mattress) );
    };


  }]);
