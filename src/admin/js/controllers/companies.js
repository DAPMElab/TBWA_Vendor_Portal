
/*  Controls the homepage where companies are listed for editting.
 **/

angular.module('app.listCompany', [])
.controller('CompanyController', function ($scope, $http, flash) {

  /*
   *  Loads all the companies to the page
   */
  $scope.initPage = function () {

    $scope.activeCompany = null;
    $http.get('/company/list/all')
      .success(function (resp) {
        console.log(resp);
        $scope.companies = resp.data;
        $scope.activeCompany = $scope.companies[0];
      })
      .error(function (err) {
        console.log(err);
        flash.post(err.message, 'alert-danger');
      });
  };
});

