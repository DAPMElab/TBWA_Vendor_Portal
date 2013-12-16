
var app = angular.module('app', [
  'app.controllers',
  'app.Values',
  'app.Services',
  'ngRoute'
]);

app.config(['$routeProvider', function($routeProvider) {
  // Declare the routes
  $routeProvider

    .when('/companies/edit/:cid', {
      templateUrl:  'admin_asset/partials/company.html',
      controller:   'EditCompanyController'
    })

    .when('/companies/new', {
      templateUrl:  'admin_asset/partials/company.html',
      controller:   'NewCompanyController'
    })

    .when('/companies', {
      templateUrl:  'admin_asset/partials/listCompany.html',
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


