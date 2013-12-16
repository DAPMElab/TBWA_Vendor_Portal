
/*
 *  Controls the page where a company is created
 */

angular.module('app.newCompany', [])
.controller('NewCompanyController', function ($scope, $http, $window,
      categories, classifications, states, setUpDict, condenseDictionary) {

  // declare scope variables
  $scope.pageTitle = 'Create New Company';
  $scope.actionButtonText = 'Create Company';
  $scope.categories = {};
  $scope.classifications = {};
  $scope.states = states;
  $scope.company = null;

  // deep watch the company object
  $scope.$watch('company', function (newVal){ /* */ }, true);

  /*
   *  Initializes the category & classification lists
   */
  $scope.initPage = function () {
    $scope.categories = setUpDict([], categories);
    $scope.classifications = setUpDict([], classifications);
  };

  /*
   *  Sends the update version to the API
   */
  $scope.pageAction = function () {
    // reform the object
    $scope.company.Categories = condenseDictionary($scope.categories);
    $scope.company.Classifications = condenseDictionary($scope.classifications);

    $http({method: 'POST', url: '/company/create', data: $scope.company})
      .success(function (resp) {
        console.log(resp);
        var cid = resp.uid;
        $window.location.href = '/admin#/companies/edit/'+cid;
      })
      .error(function (err) {
        console.log(err);
      });
  };

});

