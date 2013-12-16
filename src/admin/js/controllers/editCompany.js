
/*
 *  Controls the page where a company is editted
 */

angular.module('app.companies', [])
.controller('EditCompanyController', function ($scope, $http, $routeParams,
      categories, classifications, states, setUpDict, condenseDictionary) {

  // declare scope variables
  $scope.companyId = $routeParams.cid;
  $scope.categories = {};
  $scope.classifications = {};
  $scope.states = states;
  $scope.company = null;

  // deep watch the company object
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

  /*
   *  Sends the update version to the API
   */
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

});

