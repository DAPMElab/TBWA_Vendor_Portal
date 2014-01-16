
/*
 *  Controls the page where a company is created
 */

angular.module('app.newCompany', [])
.controller('NewCompanyController', function ($scope, $http, $window,
      availableCategories, classifications, states, setUpDict, condenseDictionary, flash) {

  // declare scope variables
  $scope.pageTitle = 'New Company Information';
  $scope.pageButtons = 'admin_asset/partials/newCompanyButtons.html';
  $scope.categories = {};
  $scope.classifications = {};
  $scope.states = states;
  $scope.company = {
    URL: 'http://',
    Videos: []
  };


  // deep watch the company object
  $scope.$watch('company', function (newVal){ /* */ }, true);

  /*
   *  Initializes the category & classification lists
   */
  $scope.initPage = function () {
    $scope.categories = setUpDict([], availableCategories);
    $scope.classifications = setUpDict([], classifications);
  };

  /*
   *  Sends the new company to the server
   */
  $scope.create = function () {
    // reform the object
    $scope.company.Categories = condenseDictionary($scope.categories);
    $scope.company.Classifications = condenseDictionary($scope.classifications);

    $http({method: 'POST', url: '/company/create', data: $scope.company})
      .success(function (resp) {
        console.log(resp);
        var cid = resp.uid;
        $window.location.href = '/admin#/companies/edit/'+cid;
        flash.post('Company created', 'alert-success');
      })
      .error(function (err) {
        console.log(err);
        flash.post(err.message, 'alert-danger');
      });
  };

  /*
   *  Adds a video to the list of videos for the company
   */
  $scope.addVideo = function () {
    // if a new video is ready and it's not a repeat video
    if ($scope.nextVideo && ($scope.company.length == 0 || $scope.company.Videos.indexOf($scope.nextVideo) == -1)){
      $scope.company.Videos.push($scope.nextVideo);
      $scope.nextVideo = "";
    }
  };

});

