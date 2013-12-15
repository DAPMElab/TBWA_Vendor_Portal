
var app = angular.module('app', [
  'app.reviews',
  'ngRoute'
]);

app.config(['$routeProvider', function($routeProvider) {
  // Declare the routes
  $routeProvider

    .when('/', {
      templateUrl:  'admin_asset/partials/reviews.html', 
      controller:   'ReviewController'})

    .otherwise({
      redirectTo: '/'
    });
}]);


