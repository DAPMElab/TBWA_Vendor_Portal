/*
 Manages the map, categories and search box
 */
angular.module('myApp.controllers', [])
.controller('SearchController',function($scope, $http, $modal, HomeSearchData,
      $routeParams, $timeout, $location, setUpDict, condenseDictionary, jobSizeRanges,
      mapRegions, mapColors, alterSVG){

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
    $scope.mapUrl = "client/img/USMap.svg";
    $scope.mapColors = mapColors;
    $scope.regions = mapRegions;
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

    $scope.sortFilters = [
        "Rating",
        "Name"
    ];

    //Category settings
    $scope.categoriesSelected = [];
    $scope.search = {"text":''};

    //Image settings
    $scope.starPhoto = "client/img/star.png";
    $scope.emptyPhoto = "client/img/starEmpty.png";


    /**
     * Executed on load of the main page to get information about each company
     */
    $scope.loadCompanies = function(){

        //query server for company info
        $http.get('/company/list').success(function(response){

            //load all as live companies
            $scope.companies = response['data'];

            //keep original companies intact when no filter is applied
            $scope.serverResponse = response['data'];

            //Create an index of each category and the corresponding companies
            for(var coIndex in $scope.companies){
                var company = $scope.companies[coIndex];

                //Uncomment below line to test star rating system
                //company['AverageReview'] = Math.floor((Math.random()*5)+1);
                var name = company['Name'];
                if (name!=null && name.length>1){
                    var categories = company['Categories'];
                    for(var catIndex in categories){
                        var category = categories[catIndex];

                        if($scope.serverResponseSortedByCategories[category]){
                            var matchingCompanies = $scope.serverResponseSortedByCategories[category];
                            var appended = matchingCompanies.concat([company]);


                            $scope.serverResponseSortedByCategories[category] = appended;
                        }else{
                            $scope.serverResponseSortedByCategories[category] = [company];
                        }
                    }
                }
            }

            //apply search params if we had them from before
            var homeData = HomeSearchData.getProperty();

            //Highlight the map and update the regions
            var regions = homeData['regions'];
            for(var regionIndex in regions){
                var region = regions[regionIndex];
                $scope.highlightMap(region);
            }

            //Add and update categories
            var categories = homeData['categories'];
            for(var catIndex in categories){
                var category = categories[catIndex];
                $scope.addCategory(category);
            }

            //Update the search text keyword
            $scope.search.text = homeData['keyword'];

            //Pick first company in the results as the selected company
            $scope.updateSelectedCompany( response.data[0] );

            //populate parameters if passed in after 1 second delay
            $timeout(function(){
                $scope.applyParameters($routeParams.param1);
            }, 1000);

        })
    };

    /**
     *Applies parameters passed through the URL
     *
     * Format is http://site/#/view/cat1=subcat,subcat2,subcat3:cat2=subcat1,subcat2,subcat3
     * Example: http://localhost:5000/#/search/cats=Casting,Distribution,Music:regs=0,1
     *
     * For categories use actual name. For regions use the number that maps to that region
     * @param routeParameters
     * @author will
     */
    $scope.applyParameters = function(routeParameters) {

        if(routeParameters!=null){
            //home/cats=asdasd,fasfasf,asasfasf,asfasf#reg=asdasd,asdasd,asdasd#stxt=asdasd
            var paramCollections = routeParameters.split(":");
            for (var paramIndex in paramCollections){
                var param = paramCollections[paramIndex];

                var equalIndex = param.indexOf("=");
                var paramCategory = param.substring(0, equalIndex);
                var paramsForCategory = param.substring(equalIndex+1, param.length).split(",");

                //regions
                if(paramCategory == "regs"){
                    for(var paramIndex in paramsForCategory){
                        var paramRegion = paramsForCategory[paramIndex];
                        $scope.highlightMap(paramRegion);
                    }

                } else if (paramCategory == "cats"){
                    for(var paramIndex in paramsForCategory){
                        var paramCat = paramsForCategory[paramIndex];
                        $scope.addCategory(paramCat);
                    }
                } else if (paramCategory == "id"){
                    $scope.updateSelectedCompanyByID(paramsForCategory);
                }
            }
        }
    };

    $scope.updateSelectedCompany = function(newSelection) {
        //$scope.selectedCompany = newSelection;
        // Send a new Get request to /company/get/uid to retrieve the rest of the information
        $http.get( '/company/get/' + newSelection['id'] ).success( function(response) {
            $scope.selectedCompany = response['data'];
        })
    };

    $scope.updateSelectedCompanyByID = function(newSelectionID) {
        //$scope.selectedCompany = newSelection;
        // Send a new Get request to /company/get/uid to retrieve the rest of the information
        $http.get( '/company/get/' + newSelectionID ).success( function(response) {
            $scope.selectedCompany = response['data'];
        })
    };

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

            //update category display
            var catElement = document.getElementById(cat);
            catElement.checked = true;
        }

        $scope.companies = newResults;

        //Reset data when no cat has been selected
        if($scope.categoriesSelected.length==0){
            $scope.companies = $scope.serverResponse;
        }
    };

    /**
     * Emails search results
     * @author will
     */
    $scope.emailSearch = function(){

        var body = '';
        var categories ='cats=';
        var regions ='regs=';

        //create categories string
        for (var index in $scope.categoriesSelected){
            var category = $scope.categoriesSelected[index];
            categories=categories+category+",";
        }

        for (var index in $scope.selectedRegionNumbers){
            var region = $scope.selectedRegionNumbers[index];
            regions=regions+region+",";
        }

        //remove last comma
        categories = categories.substring(0,categories.length-1);
        regions = regions.substring(0,regions.length-1);

        body = "http://localhost:5000/#/search/"+categories+":"+regions;

        //Send email
        window.open('mailto:.?subject=Result from search&body='+body);
    };


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

    // Doesn't interface with the backend yet
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

    $scope.test = function(stuff) {
        $location.path('search/awesome'); 
        alert($location.path());
    }

    $scope.$on('$routeUpdate', function(){
      console.log("changed");
    });

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
        var emptyCount = 5-num;
        return new Array(emptyCount);
    };

});
