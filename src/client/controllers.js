'use strict';

/* Controllers */

angular.module('myApp.controllers', []).
  controller('ReviewModalController', []);

/* Function for using Google Maps API
http://plnkr.co/edit/vfntxf?p=preview
*/
function GoogleMaps( $scope , $http , Map ) {

  $http.get('resources/map.json')
  .success(function(map_data, status, headers, config) {
    console.log('status: ', status, '\nmap_data: ', map_data, '\nconfig: ', config);
  
    Map.init(map_data,$scope);
  })
  .error(function(map_data, status, headers, config) {
    console.log('status: ', status, '\nmap_data: ', map_data, '\nconfig: ', config);
  });
  
}//GoogleMaps{}