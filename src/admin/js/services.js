
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
});

