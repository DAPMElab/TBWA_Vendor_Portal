/*
 Manages the map, categories and search box
 */
angular.module('myApp.controllers', [])
.controller('SearchController',function($scope, $http, $modal,
        $location, setUpDict, condenseDictionary, jobSizeRanges,
        mapColors, availableCategories, mapUrl, alterSVG){

    //Live companies showing after sort
    $scope.companies = [];
    $scope.jobSizeRanges = jobSizeRanges;

    //Original server data so we can undo any sorts
    $scope.serverResponse = null;
    $scope.selectedCompany = null;
    $scope.serverResponseSortedByCategories = {};
    $scope.predicate = '';
    $scope.selectedRegionNumbers = [];
    $scope.ratings=[];
    $scope.ratings.length = 5;

    //map settings
    $scope.mapUrl = mapUrl;
    $scope.mapColors = mapColors;
    $scope.activeRegions = [];

    $scope.sortFilters = [
        "Rating",
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
        var searchParams = $location.search();

        //Highlight the map and update the regions
        var regions = searchParams.regions;
        $scope.activeRegions = regions || [];
        for (regionIndex in regions) {
            alterSVG(regions[regionIndex], mapColors.highlighted);
        }

        //Add and update categories
        var paramCats = [].concat(searchParams.categories);
        $scope.categories = setUpDict(paramCats, availableCategories);

        //Update the search text keyword
        $scope.searchText = searchParams.searchText;

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
        $location.search('regions', newSearch);
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
        console.log($scope.activeRegions);
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


    /**
     * Function for modal opening
     */
    $scope.open = function () {
        $scope.newReview = {
            description: null,
            cost: null,
            category: null
        };
        $scope.reviewCategoryChoices = setUpDict([], $scope.selectedCompany.Company.Categories);
        $scope.modalInstance = $modal.open({
            templateUrl: 'client/partials/writereview.html',
            scope: $scope
        });
        console.log('modal opened');
        $scope.modalInstance.result.then(function () {
        }, function () {
            console.log('Modal dismissed at: ' + new Date());
        });
    };

    $scope.submitReview = function () {
        var data = {};
        data["Company"] = $scope.selectedCompany.Company.id;
        data["Rating"] = 5;
        data["Description"] = $scope.newReview.Description;
        data["Category"] = condenseDictionary($scope.reviewCategoryChoices);
        data["Cost"] = $scope.newReview.Cost;
        $http.post('/review/create/' + $scope.selectedCompany.Company.id, data)
            .success(function (response) {
                console.log("Review was received.");
            })
            .error(function (err) {
                console.log(err);
            });
        $scope.modalInstance.close();
    };

    $scope.setNewReviewRange = function(cost) {
        $scope.newReview['cost'] = cost;
    }

    /*
     * Rating controller
     */
    $scope.rate = 7;
    $scope.max = 10;
    $scope.isReadonly = false;

    $scope.hoveringOver = function(value) {
        $scope.overStar = value;
        $scope.percent = 100 * (value / $scope.max);
    };

    $scope.ratingStates = [
        {stateOn: 'icon-ok-sign', stateOff: 'icon-ok-circle'},
        {stateOn: 'icon-star', stateOff: 'icon-star-empty'},
        {stateOn: 'icon-heart', stateOff: 'icon-ban-circle'},
        {stateOn: 'icon-heart'},
        {stateOff: 'icon-off'}
    ];

    $scope.getNumberOfFullStars = function(num){
        return new Array(num);
    };

    $scope.getNumberOfEmptyStars = function(num){
        var emptyCount = 5 - num;
        return new Array(emptyCount);
    };

});
