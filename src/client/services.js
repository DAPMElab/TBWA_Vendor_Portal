'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', [])

// Adding service for google maps
.factory('Map', function( $rootScope , $compile ){

  var canvas   = document.getElementById('map'),
    defaults = {
      center:    new google.maps.LatLng(0,0),
      zoom:      4,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

  return {
    init:function( map_data , scope ) {

      var user_data = map_data.user.defaults,
        locations = map_data.locations,
        map_opts = {
          "center":    (typeof user_data.center !== 'undefined')
            ? new google.maps.LatLng(user_data.center[0],user_data.center[1])
            : defaults.center,
          "zoom":      (typeof user_data.zoom !== 'undefined')
            ? parseInt(user_data.zoom,10)
            : defaults.zoom,
          "mapTypeId": defaults.mapTypeId
        };
      var Map = $rootScope.map = new google.maps.Map( canvas , map_opts );
      scope.markers = [];

      for ( var count = locations.length, i = 0; i < count; i++ ) {

        var latLng  = locations[i],
          marker = new google.maps.Marker({
            position: new google.maps.LatLng( latLng[0] , latLng[1] ),
            map:      Map,
            title:    '('+latLng[0]+","+latLng[1]+')'
          }),//marker
          infowindow = new google.maps.InfoWindow();//infowindow
          scope.markers[i] = {};
          scope.markers[i].locations = [ latLng[0] , latLng[1] ];
        
        var content = '<div id="infowindow_content" ng-include src="\'infowindow.html\'"></div>';
        var compiled = $compile(content)(scope);

//console.log(scope);
        google.maps.event.addListener(
          marker,
          'click',
          (function( marker , scope, compiled , localLatLng ){
            return function(){
              scope.latLng = localLatLng;//to make data available to template
              scope.$apply();//must be inside write new values for each marker
              infowindow.setContent( compiled[0].innerHTML );
              infowindow.open( Map , marker );
            };//return fn()
          })( marker , scope, compiled , scope.markers[i].locations )
        );//addListener
        
      }//for()
    }//init
  };//return
})

//Service to transfer home search data
.factory('HomeSearchData',function(){

    var property = { Property1: 'First' };

    return {
        getProperty: function () {
            return property;
        },
        setProperty: function(value) {
            property = value;
        }
    };

})

/*
 *  Initializes a scope variable to a dictionary representing the activated values.
 *
 *  @param chosenlist: list of keys that are chosen
 *  @param choices: list of all possible keys
 *  @return: dictionary with the choices represented as true values
 */
.constant('setUpDict', function (chosenList, choices) {
    var scopeVar = {}
    // iterates over all possibles setting to false
    for (var key in choices) {
        scopeVar[choices[key]] = false;
    };
    // iterates over all chosen setting to true
    for (var key in chosenList) {
        scopeVar[chosenList[key]] = true;
    };
    return scopeVar;
})

/*
 *  Condenses the categories in $scope.categories to a single array for pashing back to the server
 *
 *  @param dict: dictionary where the value is a boolean
 *  @return: list of keys where the value was true
 */
.constant('condenseDictionary', function (dict) {
    var chosen = []; 
    for (var key in dict) {
        if (dict[key]) {
            chosen.push(key);
        }
    };
  return chosen;
})

.value('jobSizeRanges', [
    {"Range": "< $250k"},
    {"Range": "$250k - $500k"},
    {"Range": "> $500k"}
])

/*
 * SVG map constants
 * Represent the highlighted and default states of the map regions.
 */
.constant('mapColors', {
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
})

/* Regions for the SVG map
 *
 */
.constant('mapRegions', {
    0:"midwest",
    1:"southeast",
    2:"northeast",
    3:"southwest",
    4:"west"
});


