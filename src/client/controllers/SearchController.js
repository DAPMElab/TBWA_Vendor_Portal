
/*
 Manages the map, categories and search box
 */
angular.module('myApp.controllers', []).
    controller('SearchController',function($scope, $http){

        $scope.companies = [];
        $scope.serverResponse = null;
        $scope.selectedCompany = null;

        //map settings
        $scope.mapUrl = "img/USMap.svg";
        $scope.regions = {
            0:"midwest",
            1:"southeast",
            2:"northeast",
            3:"southwest",
            4:"west"
        };

        $scope.mapWidth = null;
        $scope.activeRegion = null;

        $scope.mapColors = {
            highlighted :{
                opacity :"1.0",
                fillOpacity : "1.0",
                fill : "#FFFFFF"
            },
            defaultState:{
                opacity :"0.5",
                fillOpacity : "0.5",
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
        $scope.search = {text:''};


        /**
         * Executed on load of the main page to get information about each company
        */
        $scope.loadCompanies = function(){
            $http.get('/company/list').success(function(response){

                //extract company data
                $scope.companies.serverResponse = response['data'];

                for (var companyIndex in $scope.companies.serverResponse){
                    var group = $scope.companies.serverResponse[companyIndex];
                    $scope.companies.push(group['Company']);
                }

                //By default, we pick the first company to be displayed initially
                $scope.selectedCompany = $scope.companies[0];
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

            var regionToHighlight = $scope.regions[regionNumber];

            // deselect all rooms and highlight jsut the one we want
            for (var regionIndex in $scope.regions) {

                var region = $scope.regions[regionIndex];

                // get matching svg element
                var svgElement = document.getElementById(region);

                //If proper room highlight
                if (region == regionToHighlight) {
                    svgElement.style.opacity          = $scope.mapColors.highlighted.opacity;
                    svgElement.style['fill-opacity']  = $scope.mapColors.highlighted.fillOpacity;
                    svgElement.style.fill             = $scope.mapColors.highlighted.fill;

                    $scope.activeRegion = regionToHighlight;

                    //Otherwise set to default state
                }else{
                    svgElement.style.opacity          = $scope.mapColors.defaultState.opacity;
                    svgElement.style['fill-opacity']  = $scope.mapColors.defaultState.fillOpacity;
                    svgElement.style.fill             = $scope.mapColors.defaultState.fill;
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
                $scope.categoriesSelected.splice(itemIndex);
            } else{
                $scope.categoriesSelected.push(categoryToAdd);
            }
        }

        /**
         * Main method for searching
         */
        $scope.search = function() {
            var region = $scope.activeRegion;
            var categories = $scope.categoriesSelected;
            var keyword = $scope.search.text;
        }
    });
