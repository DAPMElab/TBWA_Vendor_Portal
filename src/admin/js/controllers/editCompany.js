
/*  Controls the page where a company is editted
 **/

angular.module('app.companies', [])
.controller('EditCompanyController', function ($scope, $http, $routeParams,
      categories, classifications, states) {

  $scope.companyId = $routeParams.cid;
  $scope.categories = {};
  $scope.classifications = {};
  $scope.states = states;
  $scope.company = null;

  $scope.$watch('company', function (newVal){ /* */ }, true);


  /*
   *  Loads the company
   */
  $scope.initPage = function () {
    $http.get('/company/get/' + $scope.companyId)
      .success(function (resp) {
        $scope.company = resp.data.Company;
        $scope.categories = setUpDict($scope.company.Categories, categories);
        $scope.classifications = setUpDict($scope.company.Classifications, classifications);
      })
      .error(function (err) {
        console.log(err);
      });
  };

  $scope.updateCompany = function () {
    // reform the object
    $scope.company.Categories = condenseDictionary($scope.categories);
    $scope.company.Classifications = condenseDictionary($scope.classifications);

    $http({method: 'PATCH', url: '/company/edit/'+$scope.companyId, data: $scope.company})
      .success(function (resp) {
        console.log(resp);
      })
      .error(function (err) {
        console.log(err);
      });
  };

  /*
   *  Initializes a scope variable to a dictionary representing the activated values.
   *
   *  @param chosenlist: list of keys that are chosen
   *  @param choices: list of all possible keys
   *  @return: dictionary with the choices represented as true values
   */
  var setUpDict = function (chosenList, choices) {
    scopeVar = {}
    // iterates over all possibles setting to false
    for (var key in choices) {
      scopeVar[choices[key]] = false;
    };
    // iterates over all chosen setting to true
    for (var key in chosenList) {
      scopeVar[chosenList[key]] = true;
    };
    console.log(scopeVar);
    return scopeVar;
  };

  /*
   *  Condenses the categories in $scope.categories to a single array for pashing back to the server
   *
   *  @param dict: dictionary where the value is a boolean
   *  @return: list of keys where the value was true
   */
  var condenseDictionary = function (dict) {
    var chosen = []; 
    for (var key in dict) {
      if (dict[key]) {
        chosen.push(key);
      }
    };
    return chosen;
  };
});


