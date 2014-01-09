
/*
 *  Manages the creation and submission of company reviews
 */

angular.module('myApp.controllers')
.controller('ReviewController', function ($scope, $http, setUpDict, condenseDictionary,
  $modal, jobSizeRanges) {

    $scope.jobSizeRanges = jobSizeRanges;

    /**
     * Function for modal opening
     */
    $scope.open = function () {
        $scope.newReview = {
            Description: null,
            Cost: null,
            Category: null
        };

        $scope.reviewCategoryChoices = setUpDict([], $scope.selectedCompany.Company.Categories);
        $scope.modalInstance = $modal.open({
            templateUrl: 'client/partials/writeReview.html',
            scope: $scope
        });
    };

    $scope.submitReview = function () {
        var data = {
          Company:      $scope.selectedCompany.Company.id,
          Rating:       5, // TODO
          Description:  $scope.newReview.Description,
          Category:     condenseDictionary($scope.reviewCategoryChoices),
          Cost:         $scope.newReview.Cost,
        };
        console.log(data);
        $http.post('/review/create/' + $scope.selectedCompany.Company.id, data)
            .success(function (response) {
                console.log("Review was received.");
            })
            .error(function (err) {
                console.log(err);
            });
        $scope.modalInstance.close();
    };


    /*
     * Rating controller
     */
    $scope.rate = 7;
    $scope.max = 10;
    $scope.isReadonly = false;

    $scope.hoveringOver = function(value) {
        $scope.overStar = value;
        $scope.percent = 100 * (value / $scope.max);
    };

    $scope.ratingStates = [
        {stateOn: 'icon-ok-sign', stateOff: 'icon-ok-circle'},
        {stateOn: 'icon-star', stateOff: 'icon-star-empty'},
        {stateOn: 'icon-heart', stateOff: 'icon-ban-circle'},
        {stateOn: 'icon-heart'},
        {stateOff: 'icon-off'}
    ];

    $scope.getNumberOfFullStars = function(num){
        return new Array(num);
    };

    $scope.getNumberOfEmptyStars = function(num){
        var emptyCount = 5 - num;
        return new Array(emptyCount);
    };
});

