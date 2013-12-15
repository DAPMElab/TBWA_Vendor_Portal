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

        $routeProvider.when('/search',              {templateUrl: 'client/partials/search.html',              controller: 'SearchController'});

        //Search results
        $routeProvider.when('/map',                 {templateUrl: 'client/partials/map.html',                 controller: 'SearchController'});

        //Don't necessarily want the path, just linking up the controllers
        $routeProvider.when('/category', {templateUrl: 'client/partials/category.html', controller: 'SearchController'});
        $routeProvider.when('/currentResults', {templateUrl: 'client/partials/currentResults.html', controller: 'SearchController'});
        $routeProvider.when('/companyDescription', {templateUrl: 'client/partials/companyDescription.html', controller: 'SearchController'});
        $routeProvider.when('/companySnapshot', {templateUrl: 'client/partials/companySnapshot.html', controller: 'SearchController'});
        $routeProvider.when('/companyReviews', {templateUrl: 'client/partials/companyReviews.html', controller: 'SearchController'});
        $routeProvider.when('/home', {templateUrl: 'client/partials/home.html', controller: 'HomeController'});


        $routeProvider.otherwise({redirectTo: '/search'});
    }]);
