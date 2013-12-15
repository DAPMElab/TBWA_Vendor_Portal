'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', [
        'ngRoute',
        'myApp.filters',
        'myApp.services',
        'myApp.directives',
        'myApp.controllers',
        'ui.bootstrap'
    ]).
    config(['$routeProvider', function($routeProvider) {

        $routeProvider.when('/search', {templateUrl: 'partials/search.html', controller: 'SearchController'});

        //Search results
        $routeProvider.when('/map', {templateUrl: 'partials/map.html', controller: 'SearchController'});

        //Don't necessarily want the path, just linking up the controllers
        $routeProvider.when('/category', {templateUrl: 'partials/category.html', controller: 'SearchController'});
        $routeProvider.when('/currentResults', {templateUrl: 'partials/currentResults.html', controller: 'SearchController'});
        $routeProvider.when('/companyDescription', {templateUrl: 'partials/companyDescription.html', controller: 'SearchController'});
        $routeProvider.when('/companySnapshot', {templateUrl: 'partials/companySnapshot.html', controller: 'SearchController'});
        $routeProvider.when('/companyReviews', {templateUrl: 'partials/companyReviews.html', controller: 'SearchController'});
        $routeProvider.when('/home', {templateUrl: 'partials/home.html', controller: 'SearchController'});


        $routeProvider.otherwise({redirectTo: '/search'});
    }]);