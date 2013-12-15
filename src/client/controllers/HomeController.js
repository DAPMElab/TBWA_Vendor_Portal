/*
 Manages the map, categories and search box
 */
angular.module('myApp.controllers')
    .controller('HomeController',function($scope){

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

        //Category settings
        $scope.categoriesSelected = [];
        $scope.search = {"text":''};


        /**
         * Inits the map to a default state
         * @param mapWidth
         */
        $scope.initMap = function(mapWidth){
            $scope.mapWidth = mapWidth;
        };

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
    });
