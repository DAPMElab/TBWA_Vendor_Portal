/*
 Manages the map, categories and search box
 */
angular.module('myApp.controllers')
.controller('HomeController',function($scope, $location, $document, setUpDict,
   mapUrl, mapColors, alterSVG, availableCategories, condenseDictionary) {

    //map settings
    $scope.mapUrl = mapUrl;
    $scope.mapColors = mapColors;
    var activeRegions = [];

    //Category settings
    $scope.categories = setUpDict([], availableCategories);

    // Search box
    $scope.searchText = "";

    /**
     * Flips the highlighting of a map region
     *
     * Function is called by clicking a SVG region
     * @param region: region ID
     */
    $scope.highlightMap = function(region){
        var regionIndex = activeRegions.indexOf(region);
        if (regionIndex == -1) {
            // highlight and add to list if highlighting
            activeRegions.push(region);
            alterSVG(region, mapColors.highlighted);
        } else {
            // fade and delete from list if unhighlighting
            activeRegions.splice(regionIndex, 1);
            alterSVG(region, mapColors.defaultState);
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
        $location.search('regions', activeRegions);
        $location.search('categories', cats);
        $location.search('searchText', $scope.searchText);
    };
});
