

angular.module('app.admin', [])
.controller('NewAdminController', function ($scope, $http, $window) {

  $scope.create = function () {
    var data = { 'data': {
      email: $scope.email,
      password: $scope.password,
      repeat_password : $scope.repeatPassword
    }};

    $http.post('/admin/create', data)
      .success( function (resp) {
        console.log(resp);
        $window.location.href = '/admin#/';
      })
      .error( function (err) {
        console.log(err);
      });
  };

});

