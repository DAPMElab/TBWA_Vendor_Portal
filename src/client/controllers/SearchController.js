
/*
 Manages the map, categories and search box
 */
angular.module('myApp.controllers', []).
    controller('SearchController',function($scope, $http){

        $scope.companies = [];
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

        //$scope.availableCategories = ["Casting", "Distribution", "Production", "Translation", "Editorial", "Animation", "Post Effects", "Illustration", "Music", "Storyboarding", "Sound Design", "Directorial"];

        //Category settings
        $scope.categoriesSelected = [];
        $scope.search = {text:''};


        $scope.loadCompanies = function(){
            $http.get('/data').success(function(response){
                $scope.companies = response['data'];
                //By default, we pick the first company to be displayed initially
                $scope.selectedCompany = $scope.companies[0];
            })
        }

        $scope.updateSelectedCompany = function(selectedCompnay) {
            // jQuery to find the element in JSON array with that name
            //$scope.selectedCompany = $.grep(companies, function(company){ return company.Company == selectedCompany;});
            $scope.selectedCompany = companies[1];
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

/*
        categoriesContainsCategory = function(category) {
            for (var i = 0; i < $scope.categoriesSelected.length; i++) {
                if ($scope.categoriesSelected[i] === obj) {
                    return true;
                }
            }
            return false;
        }
*/

        /**
         * Main method for searching
         */
        $scope.search = function() {
            var region = $scope.activeRegion;
            var categories = $scope.categoriesSelected;
            var keyword = $scope.search.text;
        }
    });
