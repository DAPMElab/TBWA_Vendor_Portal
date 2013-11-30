/*
 Manages the map, categories and search box
 */
angular.module('myApp.controllers', []).
    controller('SearchController',function($scope){

        //map vars
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
            var highlighted = {
                opacity :"1.0",
                fillOpacity : "1.0",
                fill : "#2890FF"
            };

            var defaultState = {
                opacity :"0.5",
                fillOpacity : "0.5",
                fill : "#2890FF"
            };

            // deselect all rooms and highlight jsut the one we want
            for (var regionIndex in $scope.regions) {

                var region = $scope.regions[regionIndex];

                // get matching svg element
                var svgElement = document.getElementById(region);

                //If proper room highlight
                if (region == regionToHighlight) {
                    svgElement.style.opacity          = highlighted.opacity;
                    svgElement.style['fill-opacity']  = highlighted.fillOpacity;
                    svgElement.style.fill             = highlighted.fill;

                    //Otherwise set to default state
                }else{
                    svgElement.style.opacity          = defaultState.opacity;
                    svgElement.style['fill-opacity']  = defaultState.fillOpacity;
                    svgElement.style.fill             = defaultState.fill;
                }
            }
        };


    });