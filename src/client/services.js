'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', [])
  .value('version', '0.1');

// Adding service for google maps
angular.module('myApp.services', [])
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

});//