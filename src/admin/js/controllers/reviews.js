
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

        // join the applicable categories into one string for easy display
        for (var reviewIndex in $scope.reviews) {
          if ('Category' in $scope.reviews[reviewIndex]) {
            $scope.reviews[reviewIndex]['Category'] = $scope.reviews[reviewIndex]['Category'].join(', ');
          }
        };
      }).error( function(err) {
        console.log(err);
      });
  };

  /**
   * Approves a review
   *
   * @param id: database id corresponding to the review
   */
  $scope.approveReview = function (reviewIndex) {
    review = $scope.reviews[reviewIndex];
    $http.post('/review/approve/'+review.id)
      .success(function (resp) {
        $scope.reviews.splice(reviewIndex, 1); // remove from list
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
  $scope.deleteReview = function (reviewIndex) {
    review = $scope.reviews[reviewIndex];
    $http.delete('/review/delete/'+review.id)
      .success(function (resp) {
        console.log(resp);
        $scope.reviews.splice(reviewIndex, 1);  // remove from list
      })
      .error(function (err) {
        console.log(err);
      });
  };

});


