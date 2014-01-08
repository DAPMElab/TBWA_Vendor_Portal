
angular.module('app.navbar', [])
.controller('NavbarController', function ($scope, $location, $window, $http) {

  $scope.currentTab = $location.path().replace('/admin', '');

  $scope.$on("$routeChangeStart", function (event, next, current) {
    $scope.currentTab = $location.path().replace('/admin', '');
    console.log($scope.currentTab);
  });

  $scope.logout = function () {
    console.log('logging out');
    $http.post('/admin/logout')
      .success(function (resp) {
        $window.location.href = '/';
      })
      .error(function (err) {
        console.log(err);
        flash.post(err.message, 'alert-danger');
      });
  };

});

