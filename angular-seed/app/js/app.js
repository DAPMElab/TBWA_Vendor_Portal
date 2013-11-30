'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'ngRoute',
  'myApp.filters',
  'myApp.services',
  'myApp.directives',
  'myApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/header', {templateUrl: 'partials/header.html', controller: 'MyCtrl1'});
  $routeProvider.when('/mainsearch', {templateUrl: 'partials/mainsearch.html', controller: 'MyCtrl1'});
  $routeProvider.when('/search', {templateUrl: 'partials/search.html', controller: 'SearchController'});

  $routeProvider.when('/sidebar', {templateUrl: 'partials/sidebar.html', controller: 'MyCtrl1'});
  $routeProvider.otherwise({redirectTo: '/sidebar'});
}]);
