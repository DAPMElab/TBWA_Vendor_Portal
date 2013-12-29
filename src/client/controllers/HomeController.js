/*
 Manages the map, categories and search box
 */
angular.module('myApp.controllers')
.controller('HomeController',function($scope, $location, $document,
   mapColors, mapRegions, HomeSearchData, alterSVG) {

    //map settings
    $scope.mapUrl = "client/img/USMap.svg";
    $scope.regions = mapRegions;  // TODO: delete
    $scope.mapColors = mapColors;
    var activeRegions = [];

    $scope.availableCategoriesRight = [
        {"text": "Post Effects"},
        {"text": "Print Production"},
        {"text": "Production"},
        {"text": "Sound Design"},
        {"text": "Storyboarding"},
        {"text": "Translation"},
        {"text": "Other"}
    ];

    $scope.availableCategoriesLeft = [
        {"text": "Animation"},
        {"text": "Casting"},
        {"text": "Digital Production"},
        {"text": "Directorial"},
        {"text": "Distribution"},
        {"text": "Editorial"},
        {"text": "Illustration"},
        {"text": "Music"}
    ];

    //Category settings
    $scope.categoriesSelected = [];
    $scope.search = {"text":''};

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
     * Adds a category to user selected categories for company filtering
     * @param categoryToAdd
     */
    $scope.addCategory = function(categoryToAdd){
        //ask for index of item (-1) if not there
        var itemIndex = $scope.categoriesSelected.indexOf(categoryToAdd);

        //If we have, remove, otherwise add
        if(itemIndex!=-1){
            $scope.categoriesSelected.splice(itemIndex,1);
        } else{
            $scope.categoriesSelected.push(categoryToAdd);
        }

        //Update display with the new sorted categories
        var newResults = [];
        for(var catIndex in $scope.categoriesSelected){
            var cat = $scope.categoriesSelected[catIndex];

            //Append new results to previous results (from this loop)
            var matches = $scope.serverResponseSortedByCategories[cat];
            var appended = newResults.concat(matches);
            newResults=appended;
        }

        $scope.companies = newResults;

        //Reset data when no cat has been selected
        if($scope.categoriesSelected.length==0){
            $scope.companies = $scope.serverResponse;
        }
    };

    /**
     * Main method for searching
     */
    $scope.search = function() {

        //local pointers to data
        var regions = $scope.activeRegionNumbers;
        var categories = $scope.categoriesSelected;
        var keyword = $scope.search.text;

        //Set transfer data
        HomeSearchData.setProperty({regions: regions, categories:categories, keyword:keyword});

        //go to new view
        $location.path('/search');

    };
});
