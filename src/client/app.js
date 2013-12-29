'use strict';

// Declare app level module which depends on filters, and services
angular.module('myApp', [
        'ngRoute',
        'ngResource',
        'myApp.filters',
        'myApp.services',
        'myApp.directives',
        'myApp.controllers',
        'ui.bootstrap',
])
.config(['$routeProvider', function($routeProvider) {
    //Search results
    $routeProvider.when('/search', {templateUrl: 'client/partials/search.html', controller: 'SearchController'});
    // home
    $routeProvider.when('/', {templateUrl: 'client/partials/home.html', controller: 'HomeController'});

    $routeProvider.otherwise({redirectTo: '/'});
}]);
