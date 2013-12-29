/*
 Manages the map, categories and search box
 */
angular.module('myApp.controllers')
.controller('HomeController',function($scope, $location, $document, $resource,
   mapUrl, mapColors, alterSVG, availableCategories, condenseDictionary) {

    //map settings
    $scope.mapUrl = mapUrl;
    $scope.mapColors = mapColors;
    var activeRegions = [];

    //Category settings
    $scope.categories = availableCategories;

    // Search box
    $scope.searchBox = "";

    /**
     * Flips the highlighting of a map region
     *
     * Function is called by clicking a SVG region
     * @param region: abbreviation for the region represented by the svg layer
     */
    $scope.highlightMap = function(region){
        var svgElement = document.getElementById(region);
        var regionIndex = activeRegions.indexOf(region);
        if (regionIndex == -1) {
            // highlight and add to list if highlighting
            activeRegions.push(region);
            alterSVG(svgElement, mapColors.highlighted);
        } else {
            // fade and delete from list if unhighlighting
            activeRegions.splice(regionIndex, 1);
            alterSVG(svgElement, mapColors.defaultState);
        }
    };

    /**
     *  Sends the user /search and fills out the query string so the search
     *  will persist.
     */
    $scope.search = function() {
        //go to new view
        $location.path('/search');

        // set search categories
        var cats = condenseDictionary($scope.categories);
        $location.search('categories', cats);
        $location.search('keyword', $scope.searchBox);
        $location.search('regions', activeRegions);
    };
});
