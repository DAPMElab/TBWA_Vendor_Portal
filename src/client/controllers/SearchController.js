
/*
 *  Manages the map, categories and search box
 */

angular.module('myApp.controllers', [])
.controller('SearchController',function($scope, $http, $location, setUpDict,
        condenseDictionary, mapColors, availableCategories, mapUrl, alterSVG){

    var searchParams = $location.search();
    var regions =  [];
    if (searchParams.regions) {
      regions = [].concat(searchParams.regions);
    }
    $scope.activeRegions = [];
    //Add and update categories
    var paramCats = [];
    if (searchParams.categories) {
      paramCats = [].concat(searchParams.categories);
    }
    $scope.categories = setUpDict(paramCats, availableCategories);

    //Update the search text keyword
    $scope.searchText = searchParams.searchText;

    //Live companies showing after sort
    $scope.companies = [];

    //Original server data so we can undo any sorts
    $scope.selectedCompany = null;
    $scope.serverResponseSortedByCategories = {};
    $scope.predicate = '';

    //map settings
    $scope.mapUrl = mapUrl;
    $scope.mapColors = mapColors;

    $scope.sortFilters = [
        "AverageReview",
        "Name"
    ];

    //Image settings
    $scope.starPhoto = "client/img/star.png";
    $scope.emptyPhoto = "client/img/starEmpty.png";


    /**
     * Executed on load of the main page to get information about each company and
     * load the search parameters
     */
    $scope.initPage = function(){
        //Highlight the map and update the regions
        for (regionIndex in regions) {
            $scope.highlightMap(regions[regionIndex]);
        }

        //query server for company list
        $http.get('/company/list')
            .success(function (response) {
                //load all as live companies
                $scope.companies = response['data'];

                //Pick first company in the results as the selected company
                $scope.updateSelectedCompany( $scope.companies[0] );
            })
    };

    /*
     *  Watch the search values and update the query string
     */
    $scope.$watchCollection('categories', function (newCategories, oldCategories) {
        $location.search('categories', condenseDictionary(newCategories));
    });
    $scope.$watchCollection('activeRegions', function (newRegions, oldRegions) {
        $location.search('regions', newRegions);
    });
    $scope.$watch('searchText', function (newSearch, oldSearch) {
        $location.search('searchText', newSearch);
    });


    $scope.updateSelectedCompany = function(newSelection) {
        // Send a new Get request to retrieve the rest of the information
        $http.get( '/company/get/' + newSelection['id'])
            .success( function(response) {
                $scope.selectedCompany = response['data'];
            });
    };

    $scope.updateSelectedCompanyByID = function(newSelectionID) {
        // Send a new Get request to retrieve the rest of the information
        $http.get( '/company/get/' + newSelectionID )
            .success( function(response) {
                $scope.selectedCompany = response['data'];
            })
    };

    /**
     * Flips the highlighting of a map region
     *
     * Function is called by clicking a SVG region
     * @param region: region ID
     */
    $scope.highlightMap = function(region){
        var regionIndex = $scope.activeRegions.indexOf(region);
        if (regionIndex == -1) {
            // highlight and add to list if highlighting
            $scope.activeRegions.push(region);
            alterSVG(region, mapColors.highlighted);
        } else {
            // fade and delete from list if unhighlighting
            $scope.activeRegions.splice(regionIndex, 1);
            alterSVG(region, mapColors.defaultState);
        }
    };

    /**
     * Emails search results
     */
    $scope.emailSearch = function(){
        body = $location.absUrl();
        window.open('mailto:.?subject=Result from search&body='+body);
    };

    /**
     * Updates what the search results are ordered by
     */
    $scope.updatePredicate = function(filter){
        $scope.predicate = filter;
    };
});

