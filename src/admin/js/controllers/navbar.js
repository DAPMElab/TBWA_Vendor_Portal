
angular.module('app.navbar', [])
.controller('NavbarController', function ($scope, $location) {

  $scope.currentTab = $location.path().replace('/admin', '');

  $scope.$on("$routeChangeStart", function (event, next, current) {
    $scope.currentTab = $location.path().replace('/admin', '');
    console.log($scope.currentTab);
  });

});

