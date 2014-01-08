
angular.module('app.Services', [])

/*
 *  Initializes a scope variable to a dictionary representing the activated values.
 *
 *  @param chosenlist: list of keys that are chosen
 *  @param choices: list of all possible keys
 *  @return: dictionary with the choices represented as true values
 */
.constant('setUpDict', function (chosenList, choices) {
  scopeVar = {}
  // iterates over all possibles setting to false
  for (var key in choices) {
    scopeVar[choices[key]] = false;
  };
  // iterates over all chosen setting to true
  for (var key in chosenList) {
    if (chosenList[key]) {  // prevent empty keys
      scopeVar[chosenList[key]] = true;
    }
  };
  return scopeVar;
})

/*
 *  Condenses the categories in $scope.categories to a single array for pashing back to the server
 *
 *  @param dict: dictionary where the value is a boolean
 *  @return: list of keys where the value was true
 */
.constant('condenseDictionary', function (dict) {
  var chosen = []; 
  for (var key in dict) {
    if (dict[key]) {
      chosen.push(key);
    }
  };
  return chosen;
})

/*
 *  Controls boostrap alerts
 *
 *  Flashes a message for 5 seconds. Requires a message and an alert type to post.
 *  type options: [
 *    alert-success
 *    alert-info
 *    alert-warning
 *    alert-danger
 *  ]
 */
.factory('flash', function ($rootScope, $timeout) {
  var message = "",
      alertType = "";
  $rootScope.displayAlert = false;

  return {
    // posts a flash alert
    post : function (msg, type) {
      message = msg;
      alertType = type;
      $rootScope.displayAlert = true;

      $timeout( // clear message after 5 seconds
        function () {
          $rootScope.displayAlert = false;
        }, 1000 * 5 // 5 seconds
      );
    },
    // returns the current flash alert
    get : function () {
      return {
        'message': message,
        'alertType': alertType
      };
    }
  };
});

