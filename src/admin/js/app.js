
var app = angular.module('app', [
  'app.reviews',
  'app.companies',
  'app.Values',
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


