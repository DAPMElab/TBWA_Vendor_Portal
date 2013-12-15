
var app = angular.module('app', [
  'app.reviews',
  'app.companies',
  'ngRoute'
]);

app.config(['$routeProvider', function($routeProvider) {
  // Declare the routes
  $routeProvider

    .when('/companies', {
      templateUrl:  'admin_asset/partials/companies.html',
      controller:   'CompanyController'
    })

    .when('/', {
      templateUrl:  'admin_asset/partials/reviews.html', 
      controller:   'ReviewController'
    })

    .otherwise({
      redirectTo: '/'
    });
}]);


