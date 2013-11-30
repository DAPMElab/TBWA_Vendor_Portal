
angular.module('app', [
	// list dependencies
]).config(['$routeProvidor', function($routeProvidor) {
        
	// declare each route
        $routeProvider.when('/login', {templateUrl: 'partials/login.html', controller: 'LoginController'});
        $routeProvider.when('/admin', {templateUrl: 'partials/admin_console.html', controller: 'AdminController'});
        $routeProvider.when('/home', {templateUrl: 'partials/home.html', controller: 'HomeController'});
        $routeProvider.when('/review', {templateUrl: 'partials/review.html', controller: 'ReviewController'});
        $routeProvider.when('/search', {templateUrl: 'partials/search.html', controller: 'SearchController'});

        $routeProvider.otherwise({redirectTo: '/search'});
}]);

