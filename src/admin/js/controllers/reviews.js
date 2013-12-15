
/*  Controls the homepage where unapproved reviews are shown.
 **/

angular.module('app.reviews', [])
.controller('ReviewController', function ($scope, $http) {

  /*  
   *  Loads all relevevant data for the page on initialization
   */
  $scope.initPage = function (){
    $http.get('/review/list')
      .success( function(response) {
        console.log(response);
        $scope.reviews = response['data'];
      }).error( function(err) {
        console.log(err);
      });
  };

  /**
   * Approves a review
   *
   * @param id: database id corresponding to the review
   */
  $scope.approveReview = function (id) {
    $http.post('/review/approve/'+id)
      .success(function (resp) {
        console.log(resp);
      })
      .error(function (err) {
        console.log(err);
      });
  };
  
  /**
   * Deletes a review
   *
   * @param id: database id corresponding to the review
   */
  $scope.deleteReview = function (id) {
    $http.delete('/review/delete/'+id)
      .success(function (resp) {
        console.log(resp);
      })
      .error(function (err) {
        console.log(err);
      });
  };

});


