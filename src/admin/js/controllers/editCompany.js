
/*
 *  Controls the page where a company is edited
 */

angular.module('app.editCompany', [])
.controller('EditCompanyController', function ($scope, $http, $routeParams, $location,
      availableCategories, classifications, states, setUpDict, condenseDictionary, flash) {

  // declare scope variables
  $scope.pageTitle = 'Editing Company -';
  $scope.pageButtons = 'admin_asset/partials/editCompanyButtons.html';
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
        console.log(resp);
        $scope.company = resp.data.Company;
        $scope.categories = setUpDict($scope.company.Categories, availableCategories);
        $scope.classifications = setUpDict($scope.company.Classifications, classifications);
      })
      .error(function (err) {
        console.log(err);
        $location.path('/companies');
      });
  };

  /*
   *  Sends the update version to the API
   */
  $scope.update = function () {
    // reform the object
    $scope.company.Categories = condenseDictionary($scope.categories);
    $scope.company.Classifications = condenseDictionary($scope.classifications);

    $http({method: 'PATCH', url: '/company/edit/'+$scope.companyId, data: $scope.company})
      .success(function (resp) {
        console.log(resp);
        flash.post('Company Updated', 'alert-info');
      })
      .error(function (err) {
        console.log(err);
      });
  };

  /*
   *  Deletes the company
   */
  $scope.delete = function () {
    $http.delete('/company/delete/'+$scope.companyId)
      .success( function (data) {
        console.log(data);
        $location.path('/companies');
      })
      .error( function (err) {
        console.log(err);
      });
  };

  /*
   *  Adds a video to the list of videos for the company
   */
  $scope.addVideo = function () {
    // if a new video is ready and it's not a repeat video
    if ($scope.nextVideo && ($scope.company.length == 0 || $scope.company.videos.indexOf($scope.nextVideo) == -1)){
      $scope.company.videos.push($scope.nextVideo);
      $scope.nextVideo = "";
    }
  };

});

