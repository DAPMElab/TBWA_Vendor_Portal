/*
 Manages the map, categories and search box
 */
angular.module('myApp.controllers', [])
    .controller('SearchController',function($scope, $http, $modal, HomeSearchData){

        //Live companies showing after sort
        $scope.companies = [];

        //Original server data so we can undo any sorts
        $scope.serverResponse = null;
        $scope.selectedCompany = null;
        $scope.serverResponseSortedByCategories = {};
        $scope.predicate = '';

        //map settings
        $scope.mapUrl = "client/img/USMap.svg";
        $scope.regions = {
            0:"midwest",
            1:"southeast",
            2:"northeast",
            3:"southwest",
            4:"west"
        };

        $scope.mapWidth = null;
        $scope.activeRegions = [];

        $scope.mapColors = {
            highlighted :{
                opacity :"1.0",
                fillOpacity : "1.0",
                fill : "#66CCFF"
            },
            defaultState:{
                opacity :"1.0",
                fillOpacity : "1.0",
                fill : "#FFFFFF"
            }
        };

        $scope.availableCategories = [
            {"text": "Casting"},
            {"text": "Distribution"},
            {"text": "Production"},
            {"text": "Translation"},
            {"text": "Editorial"},
            {"text": "Animation"},
            {"text": "Post Effects"},
            {"text": "Illustration"},
            {"text": "Music"},
            {"text": "Storyboarding"},
            {"text": "Sound Design"},
            {"text": "Directorial"}
        ];

        $scope.sortFilters = [
            "Rating",
            "Name"
        ];

        //Category settings
        $scope.categoriesSelected = [];
        $scope.search = {"text":''};

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

                //By default, we pick the first company to be displayed initially
                $scope.selectedCompany = $scope.companies[0];

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

                $scope.search.text = homeData['keyword'];
            })
        }

        $scope.updateSelectedCompany = function(newSelection) {
            $scope.selectedCompany = newSelection;
        }

        /**
         * Inits the map to a default state
         * @param mapWidth
         */
        $scope.initMap = function(mapWidth){
            $scope.mapWidth = mapWidth;
        }

        /**
         * Highlights a svg xml tag using the element id
         * It deselects everything first, then highlights the item requested. The highlight is done by adjusting the alpha
         *
         * @param regionNumber
         * @author will
         */
        $scope.highlightMap = function(regionNumber){

            //track added regions
            var regionToHighlight = $scope.regions[regionNumber];

            var index = $scope.activeRegions.indexOf(regionToHighlight);
            if(index==-1){
                $scope.activeRegions.push(regionToHighlight);

            }else{
                $scope.activeRegions.splice(index,1);

            }


            //Deselect all regions
            var svgChilren = document.getElementsByTagName("path");
            for (var childIndex in svgChilren){
                var child = svgChilren[childIndex];
                if(child.style!=null){
                    child.style.fill = $scope.mapColors.defaultState.fill;

                }
            }

            // deselect all rooms and highlight jsut the one we want
            for (var regionIndex in $scope.activeRegions) {

                var region = $scope.activeRegions[regionIndex];

                // get matching svg element
                var svgElement = document.getElementById(region);

                svgElement.style.opacity          = $scope.mapColors.highlighted.opacity;
                svgElement.style['fill-opacity']  = $scope.mapColors.highlighted.fillOpacity;
                svgElement.style.fill             = $scope.mapColors.highlighted.fill;

                $scope.activeRegion = regionToHighlight;

                //Change the colors of the actual region by going into each path node
                var svgChilren = svgElement.getElementsByTagName("path");
                for (var childIndex in svgChilren){
                    var child = svgChilren[childIndex];

                    if(child.style!=null){
                        child.style.fill = $scope.mapColors.highlighted.fill;

                    }
                }
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
            var region = $scope.activeRegion;
            var categories = $scope.categoriesSelected;
            var keyword = $scope.search.text;
        };

        $scope.updatePredicate = function(filter){
            $scope.predicate = filter;
        };


        $scope.items = ['item1', 'item2', 'item3'];
        $scope.selected = {};
        $scope.open = function () {
            var modalInstance = $modal.open({
                templateUrl: 'client/partials/writereview.html',
                scope: $scope
            });
            console.log('modal opened');
            modalInstance.result.then(function () {
                console.log($scope.selected);
            }, function () {
                console.log('Modal dismissed at: ' + new Date());
            });
        };

    });
